from typing import List

from flask import Response, jsonify
from sqlalchemy import create_engine, Column, String, Date, Numeric, DateTime, Float, delete, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

from app import app, Constants
from app.model.analytics_chart import AnalyticsChart

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
    def run_query(start_date, end_date) -> List[AnalyticsChart]:
        # Connect to your MySQL database using SQLAlchemy
        engine = create_engine('your_database_connection_string')

        # Define your raw SQL query with parameters
        sql_query = text("""
            SELECT 
                vendor, 
                MONTH(purchased_at) AS month,
                YEAR(purchased_at) AS year,
                FORMAT(SUM(total), 2) AS total_amount,
                (SELECT FORMAT(SUM(total), 2) FROM operations_receipts WHERE MONTH(purchased_at) = :month AND YEAR(purchased_at) = :year) AS total_amount_month,
                FORMAT(SUM(sub_total), 2) AS total_sub_total,
                (SELECT FORMAT(SUM(sub_total), 2) FROM operations_receipts WHERE MONTH(purchased_at) = :month AND YEAR(purchased_at) = :year) AS total_sub_amount_month,
                FORMAT(SUM(tax), 2) AS total_tax,
                (SELECT FORMAT(SUM(tax), 2) FROM operations_receipts WHERE MONTH(purchased_at) = :month AND YEAR(purchased_at) = :year) AS total_tax_month
            FROM 
                operations_receipts 
            WHERE  
                purchased_at BETWEEN :start_date AND :end_date
            GROUP BY 
                vendor, 
                MONTH(purchased_at)
            ORDER BY 
                MONTH(purchased_at) ASC;
        """)

        # Execute the query using SQLAlchemy's execute() method
        with engine.connect() as conn:
            results = conn.execute(sql_query, start_date=start_date, end_date=end_date, month=start_date.month,
                                   year=start_date.year).fetchall()

        # Create list of AnalyticsChart objects from the query results
        analytics_charts = []
        for row in results:
            analytics_chart = AnalyticsChart(
                row['vendor'],
                row['month'],
                row['year'],
                float(row['total_amount']),
                float(row['total_amount_month']),
                float(row['total_sub_total']),
                float(row['total_sub_amount_month']),
                float(row['total_tax']),
                float(row['total_tax_month'])
            )
            analytics_charts.append(analytics_chart)

        return analytics_charts

