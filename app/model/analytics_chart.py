
class AnalyticsChart:
    vendor: str
    month: int
    year: int
    total_amount: float
    total_amount_month: float
    total_amount_subtotal: float
    total_amount_subtotal_month: float
    total_tax: float
    total_tax_month: float

    @classmethod
    def empty(cls):
        return cls("", 0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0)

    def __init__(self, vendor: str, month: int, year: int, total_amount: float, total_amount_month: float,
                 total_amount_subtotal: float, total_amount_subtotal_month: float, total_tax: float,
                 total_tax_month: float) -> None:
        self.vendor = vendor
        self.month = month
        self.year = year
        self.total_amount = total_amount
        self.total_amount_month = total_amount_month
        self.total_amount_subtotal = total_amount_subtotal
        self.total_amount_subtotal_month = total_amount_subtotal_month
        self.total_tax = total_tax
        self.total_tax_month = total_tax_month

    def __str__(self) -> str:
        return (
            f'vendor: {self.vendor}, month: {self.month}, year: {self.year}, total_amount: {self.total_amount}, '
            f'total_amount_month: {self.total_amount_month}, total_amount_subtotal: {self.total_amount_subtotal}, '
            f'total_amount_subtotal_month: {self.total_amount_subtotal_month}, total_tax: {self.total_tax}, total_tax_month: {self.total_tax_month}')



