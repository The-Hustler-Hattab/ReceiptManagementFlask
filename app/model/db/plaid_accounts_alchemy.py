from datetime import datetime, date
from typing import List

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.model.db.receipts_alchemy import session, Base


class PlaidAccounts(Base):
    __tablename__ = 'plaid_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    institution_id = Column(Integer, ForeignKey('plaid_institution_access_tokens.id'), nullable=False)
    account_id = Column(String(255), nullable=False)
    mask = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    subtype = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    access_token = relationship("PlaidInstitutionAccessTokens", back_populates="accounts")

    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "mask": self.mask,
            "name": self.name,
            "type": self.type,
            "subtype": self.subtype,
            "created_at": self._serialize_date(self.created_at),
        }

    @staticmethod
    def _serialize_date(value):
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value

    @staticmethod
    def save_plaid_account_to_db(plaidAccount: 'PlaidAccounts') -> int:
        try:
            session.add(plaidAccount)
            # Commit the session to persist the object in the database
            session.commit()
            print("[+] PlaidAccounts saved to db")
            return plaidAccount.id

        except Exception as e:
            session.rollback()
            print(f'Error committing to the db: {e}')
            raise e

    @staticmethod
    def save_all_accounts_to_db(accounts: List['PlaidAccounts']) -> None:
        try:
            # Iterate over the list of Property objects
            for account in accounts:
                session.add(account)

            # Commit the session to persist all objects in the database
            session.commit()
            print("[+] All accounts saved to db")
        except Exception as e:
            # Rollback in case of any error
            session.rollback()
            print(f'Error committing the list to the db: {e}')
            raise e

