from typing import List

from flask import Response, jsonify
from sqlalchemy import create_engine, Column, String, Date, Numeric, DateTime, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

from app import app, Constants
from app.model.charts.bar_chart import BarChart
from app.model.charts.horizantal_chart import HorizontalChart
from app.model.charts.line_chart import LineChart
from app.model.charts.pie_chart import PieChart

# Create a base class for our declarative models
Base = declarative_base()

engine = create_engine(app.config.get(Constants.MYSQL_URL))

Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


class Receipt:
    file_path: str
    total: float
    sub_total: float
    tax: float
    company_name: str
    vendor: str
    created_by: str
    created_at: datetime.date
    purchased_at: datetime.date
    vendor_address: str
    customer_name: str
    invoice_id: str

    # def __init__(self) -> None:
    #     pass

    def __init__(self, file_path: str, total: float, sub_total: float, tax: float, vendor: str, company_name: str,
                 created_by: str, purchased_at: datetime.date, vendor_address: str, customer_name: str,
                 invoice_id: str) -> None:
        self.file_path = file_path
        self.total = total
        self.sub_total = sub_total
        self.tax = tax
        self.company_name = company_name
        self.vendor = vendor
        self.purchased_at = purchased_at
        self.vendor_address = vendor_address
        self.customer_name = customer_name
        self.invoice_id = invoice_id
        self.created_by = created_by

    def __str__(self) -> str:
        return (
            f'file_path: {self.file_path}, total: {self.total}, sub_total: {self.sub_total}, tax: {self.tax}, vendor: {self.vendor}, '
            f'company_name: {self.company_name}, created_by: {self.created_by}, purchased_at: {self.purchased_at}, vendor_address: {self.vendor_address}')

    @classmethod
    def empty(cls):
        return cls("", None, None, None, "", ""
                   , "", None, "", "", "")

    def convert_to_receipts_alchemy(self) -> object:
        return Receipts(file_path=self.file_path, total=self.total,
                        sub_total=self.sub_total, tax=self.tax,
                        company_name=self.company_name,
                        vendor=self.vendor, created_by=self.created_by,
                        purchased_at=self.purchased_at, vendor_address=self.vendor_address,
                        customer_name=self.customer_name, invoice_id=self.invoice_id)


class Receipts(Base):
    __tablename__ = 'operations_receipts'

    id: int = Column(Numeric, primary_key=True, nullable=False)
    file_path: str = Column(String(500), nullable=False)
    total: float = Column(Float, nullable=False)
    sub_total: float = Column(Float, nullable=False)
    tax: float = Column(Float, nullable=False)
    vendor: str = Column(String(200), nullable=False)
    created_at: str = Column(DateTime, nullable=False, default=datetime.now)
    created_by: str = Column(String(200), nullable=False, default="ReceiptsAlchemy")
    company_name: str = Column(String(200), nullable=False)
    purchased_at: Date = Column(Date, nullable=False)
    vendor_address: str = Column(String(2000), nullable=True)
    customer_name: str = Column(String(200), nullable=True)
    invoice_id: str = Column(String(200), nullable=True)

    def __str__(self) -> str:
        return (
            f'id: {self.id}, file_path: {self.file_path}, total: {self.total}, sub_total: {self.sub_total}, tax: {self.tax}, vendor: {self.vendor}, '
            f'created_at: {self.created_at}, created_by: {self.created_by} '
            f'company_name: {self.company_name} purchased_at: {self.purchased_at} vendor_address: {self.vendor_address}')

    def to_dict(self):
        return {
            'id': str(self.id),
            'file_path': self.file_path,
            'total': float(self.total),
            'sub_total': float(self.sub_total),
            'tax': float(self.tax),
            'vendor': self.vendor,
            'created_at': str(self.created_at),
            'created_by': self.created_by,
            'company_name': self.company_name,
            'purchased_at': str(self.purchased_at),
            'vendor_address': self.vendor_address,
            'customer_name': self.customer_name,
            'invoice_id': self.invoice_id
        }

    @staticmethod
    def convert_receipts_to_dicts(receipts) -> list[dict]:
        """
        Convert list of Receipts objects to a list of dictionaries.

        Args:
            receipts (list): List of Receipts objects.

        Returns:
            list: List of dictionaries representing each Receipts object.
        """
        receipts_list = []
        for receipt in receipts:
            receipt_dict = receipt.to_dict()
            receipts_list.append(receipt_dict)
        return receipts_list

    @staticmethod
    def get_all() -> list[object]:
        session.close()
        return session.query(Receipts).all()

    @staticmethod
    def save_receipt_to_db(receipt: Receipt) -> None:
        try:
            # Create an EmailCreds object
            alchemy_receipt = receipt.convert_to_receipts_alchemy()
            # Add the object to the session
            session.add(alchemy_receipt)
            # Commit the session to persist the object in the database
            session.commit()
            print("[+] Receipt saved to db")
        except Exception as e:
            session.rollback()
            print(f'Error committing to the db: {e}')
            raise e

    @staticmethod
    def delete_by_file_path(file_path: str) -> tuple[Response, int]:
        session = Session()
        try:
            receipts_to_delete = session.query(Receipts).filter_by(file_path=file_path).all()
            deleted_count = len(receipts_to_delete)
            for receipt in receipts_to_delete:
                session.delete(receipt)
            session.commit()

            if deleted_count > 0:
                print(f"[+] {deleted_count} receipt(s) with file_path '{file_path}' deleted from the database.")
                return jsonify({'message': f'Receipt(s) with file_path "{file_path}" deleted successfully'}), 200
            else:
                print(f"[-] No receipts found with file_path '{file_path}'.")
                return jsonify({'message': f'No receipt found with file_path "{file_path}"'}), 404

        except Exception as e:
            session.rollback()
            print(f'Error deleting from the db: {e}')
            return jsonify({'message': f'Failed to delete receipt(s) with file_path "{file_path}": {e}'}), 500

    @staticmethod
    def fetch_between_bar_chart_model_non_null_vendors(start_date: date, end_date: date) -> List[BarChart]:
        # Define your raw SQL query with parameters
        sql_query = text("""
    SELECT * FROM (SELECT 
    vendors.vendor,
    months.month,
    years.year,
    IFNULL(FORMAT(SUM(op.total), 2), '0.00') AS total_amount,
        IFNULL((
        SELECT 
           FORMAT(SUM(total), 2) 
        FROM 
            operations_receipts 
        WHERE 
            MONTH(purchased_at) = month
            AND YEAR(purchased_at) = year
    ),0.00) AS total_amount_month,
    IFNULL(FORMAT(SUM(op.sub_total), 2), '0.00') AS total_sub_total,
    IFNULL( 
            (
        SELECT 
            FORMAT(SUM(sub_total), 2) 
        FROM 
            operations_receipts 
        WHERE 
            MONTH(purchased_at) = month
            AND YEAR(purchased_at) = year
    ), '0.00') AS total_sub_amount_month,
    IFNULL(FORMAT(SUM(op.tax), 2), '0.00') AS total_tax,
    IFNULL((
        SELECT 
            FORMAT(SUM(tax), 2) 
        FROM 
            operations_receipts 
        WHERE 
            MONTH(purchased_at) = month
            AND YEAR(purchased_at) = year
    ), '0.00') AS total_tax_month,
    ifNull(
        DATE_FORMAT(IFNULL(op.purchased_at, CONCAT_WS('-', years.year, months.month, '01')), '%Y-%m-%d'),
        'NULL'
    ) as purchased_at  
FROM 
    (
        SELECT DISTINCT vendor FROM operations_receipts
    ) AS vendors
CROSS JOIN 
    (
        SELECT 1 AS month UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL
        SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12
    ) AS months
CROSS JOIN 
    (
        SELECT YEAR(purchased_at) AS year FROM operations_receipts where purchased_at   GROUP BY YEAR(purchased_at)
    ) AS years
LEFT JOIN 
    operations_receipts op 
    ON op.vendor = vendors.vendor 
    AND MONTH(op.purchased_at) = months.month 
    AND YEAR(op.purchased_at) = years.year 
GROUP BY 
    vendors.vendor, 
    months.month, 
    years.year
ORDER BY 
    years.year ASC, months.month ASC) AS data
   
    where data.purchased_at BETWEEN :start_date AND :end_date
    ;
        """)

        # Execute the query using SQLAlchemy's execute() method
        with engine.connect() as conn:
            results = conn.execute(sql_query, {'start_date': start_date, 'end_date': end_date}).fetchall()

        # Create list of AnalyticsChart objects from the query results
        analytics_charts = []
        for row in results:
            analytics_chart = BarChart(
                row[0],  # vendor
                row[1],  # month
                row[2],  # year
                float(row[3]),  # total_amount
                float(row[4]),  # total_amount_month
                float(row[5]),  # total_sub_total
                float(row[6]),  # total_sub_amount_month
                float(row[7]),  # total_tax
                float(row[8])  # total_tax_month
            )
            analytics_charts.append(analytics_chart)

        return analytics_charts

    @staticmethod
    def fetch_between_pie_chart_model(start_date: date, end_date: date) -> List[PieChart]:
        # Define your raw SQL query with parameters
        sql_query = text("""
    SELECT 
        vendor,
        ROUND(SUM(total), 2) AS total_sum,
        ROUND(SUM(sub_total), 2) AS sub_total_sum,
        ROUND(SUM(tax), 2) AS tax_sum
    from operations_receipts WHERE 
    purchased_at BETWEEN :start_date AND :end_date
    group by vendor;
        """)

        # Execute the query using SQLAlchemy's execute() method
        with engine.connect() as conn:
            results = conn.execute(sql_query, {'start_date': start_date, 'end_date': end_date}).fetchall()

        # Create list of AnalyticsChart objects from the query results
        analytics_charts = []
        for row in results:
            analytics_chart = PieChart(
                row[0],  # vendor
                float(row[1]),  # total_amount
                float(row[2]),  # total_sub_total
                float(row[3]),  # total_tax
            )
            analytics_charts.append(analytics_chart)

        return analytics_charts


    @staticmethod
    def fetch_between_line_chart_model(start_date: date, end_date: date) -> List[LineChart]:
        # Define your raw SQL query with parameters
        sql_query = text("""
SELECT 
    YEAR(purchased_at) AS year,
    MONTH(purchased_at) AS month,
    ROUND(SUM(total), 2) AS total_cost,
    ROUND(SUM(sub_total), 2) AS total_sub_total,
    ROUND(SUM(tax), 2) AS total_tax,
    (ROUND(SUM(total), 2) + 
     LAG(ROUND(SUM(total), 2), 1, 0) OVER (ORDER BY YEAR(purchased_at), MONTH(purchased_at))) AS overall_total_cost,
    (ROUND(SUM(sub_total), 2) + 
     LAG(ROUND(SUM(sub_total), 2), 1, 0) OVER (ORDER BY YEAR(purchased_at), MONTH(purchased_at))) AS overall_total_sub_total,
    (ROUND(SUM(tax), 2) + 
     LAG(ROUND(SUM(tax), 2), 1, 0) OVER (ORDER BY YEAR(purchased_at), MONTH(purchased_at))) AS overall_total_tax
FROM 
    operations_receipts
    
    where purchased_at BETWEEN :start_date AND :end_date
    
GROUP BY 
    YEAR(purchased_at), MONTH(purchased_at)
ORDER BY 
    YEAR(purchased_at), MONTH(purchased_at);
        """)

        # Execute the query using SQLAlchemy's execute() method
        with engine.connect() as conn:
            results = conn.execute(sql_query, {'start_date': start_date, 'end_date': end_date}).fetchall()

        # Create list of AnalyticsChart objects from the query results
        analytics_charts = []
        for row in results:
            analytics_chart = LineChart(
                int(row[0]),  # year
                int(row[1]),  # month
                round(float(row[5]),2),  # over_all_total_cost
                round(float(row[6]),2),  # over_all_total_sub_total
                round(float(row[7]),2),  # over_all_total_tax
            )
            analytics_charts.append(analytics_chart)

        return analytics_charts

    @staticmethod
    def fetch_between_horizontal_chart_model(start_date: date, end_date: date) -> List[HorizontalChart]:
        # Define your raw SQL query with parameters
        sql_query = text("""
SELECT 
    YEAR(purchased_at) AS year,
    MONTH(purchased_at) AS month,
    ROUND(SUM(total),2 )AS total_cost,
    ROUND(SUM(sub_total),2) AS total_sub_total,
    ROUND(SUM(tax),2) AS total_tax
FROM 
    operations_receipts where purchased_at BETWEEN :start_date AND :end_date
GROUP BY 
    YEAR(purchased_at), MONTH(purchased_at)
ORDER BY 
    YEAR(purchased_at), MONTH(purchased_at);
        """)

        # Execute the query using SQLAlchemy's execute() method
        with engine.connect() as conn:
            results = conn.execute(sql_query, {'start_date': start_date, 'end_date': end_date}).fetchall()

        # Create list of AnalyticsChart objects from the query results
        analytics_charts = []
        for row in results:
            analytics_chart = HorizontalChart(
                int(row[0]),  # year
                int(row[1]),  # month
                round(float(row[2]), 2),  # total_cost
                round(float(row[3]), 2),  # total_sub_total
                round(float(row[4]), 2),  # total_tax
            )
            analytics_charts.append(analytics_chart)

        return analytics_charts
