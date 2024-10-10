import logging
from datetime import datetime, date

from flask import jsonify
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.products import Products
from plaid.model.transactions_get_request import TransactionsGetRequest

from app import client
from app.model.db.plaid_access_token_alchemy import PlaidInstitutionAccessTokens
from app.model.db.plaid_accounts_alchemy import PlaidAccounts
from app.util.data_manipulation import DataManipulation
from app.util.jwt_utls import get_user_email
import concurrent.futures

log = logging.getLogger('PlaidService')
class PlaidService:


    @staticmethod
    def create_link_token():
        try:
            user_email = get_user_email()
            # user_email = 'test'

            print("user email: " + user_email)
            user_email_hashed = DataManipulation.get_sha256_hash(user_email)
            print("user email hashed: " + user_email_hashed)
            # Create the request object for Plaid's link_token_create endpoint
            link_token_request = LinkTokenCreateRequest(
                client_name="Hattab LLC",
                language="en",
                country_codes=[CountryCode('US')],  # Correct way to initialize CountryCode
                user={
                    "client_user_id": user_email_hashed  # A unique ID for the user in your system

                },
                products=[Products("auth"), Products("transactions")]  # Use Products enum values here
            )

            # Call Plaid's link token create API
            response = client.link_token_create(link_token_request)

            # Return the generated link token
            return jsonify({"link_token": response['link_token'], "expiration": response['expiration'],
                            "request_id": response['request_id']}), 200

        except Exception as e:
            log.info(f"Error creating link token: {str(e)}")
            # raise e
            return jsonify({"error": "Internal server error"}), 500
    @staticmethod
    def create_access_token(data):
        try:
            # Parse JSON body to extract the public_token
            public_token = data.get('public_token')
            institution_id = data.get('institution_id')
            institution_name = data.get('institution_name')
            accounts = data['accounts']

            log.info(f"[+] data: {data}")

            # Validate if public_token is present
            if not public_token:
                return jsonify({"error": "Missing public_token"}), 400

            # Create the request object for exchanging the public token
            exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)

            # Call Plaid's API to exchange the public token for an access token
            response = client.item_public_token_exchange(exchange_request)

            # Extract the access token and item_id from the response
            access_token = response['access_token']
            item_id = response['item_id']

            PlaidService.save_access_token_in_db(access_token, accounts, institution_id, institution_name, item_id,
                                                 response)

            # Return the access token and item ID
            return jsonify({"message": "Access token created successfully"}), 200

        except Exception as e:

            log.error(f"Error exchanging public token: {str(e)}")
            if str(e).__contains__("Status Code: 400"):
                return jsonify({"message": "Invalid public token"}), 400

            return jsonify({"message": "Internal server error"}), 500

    @staticmethod
    def save_access_token_in_db(access_token, accounts, institution_id, institution_name, item_id, response):
        plaidInstitutionAccessTokens: 'PlaidInstitutionAccessTokens' = PlaidInstitutionAccessTokens()
        plaidInstitutionAccessTokens.access_token = access_token
        plaidInstitutionAccessTokens.institution_id = institution_id
        plaidInstitutionAccessTokens.institution_name = institution_name
        plaidInstitutionAccessTokens.created_by = get_user_email()
        plaidInstitutionAccessTokens.item_id = item_id
        primary_key = PlaidInstitutionAccessTokens.save_access_token_to_db(plaidInstitutionAccessTokens)
        log.info(f"[+] Response: {response}")
        accounts_to_save = []
        # Save each account to the database
        for account in accounts:
            new_account = PlaidAccounts(
                institution_id=primary_key,
                account_id=account['id'],
                mask=account['mask'],
                name=account['name'],
                subtype=account['subtype'],
                type=account['type'],
                created_at=datetime.now()
            )
            accounts_to_save.append(new_account)
        PlaidAccounts.save_all_accounts_to_db(accounts_to_save)


    @staticmethod
    def get_transactions_and_balance(bank_id: int, start_date: str, end_date: str):
        # Fetch the access token from the database
        access_token = PlaidInstitutionAccessTokens.get_access_token_by_id(bank_id)
        if not access_token:
            return jsonify({'message': 'Bank ID not found'}), 404
        try:
            # Create a ThreadPoolExecutor to run tasks concurrently
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Schedule both the get_transactions and get_balance functions to run concurrently
                transactions_future = executor.submit(PlaidService.get_transactions, access_token, end_date, start_date)
                balance_future = executor.submit(PlaidService.get_balance, access_token)

                # Wait for both to complete and get the results
                serialized_transactions, total_transactions = transactions_future.result()
                serialized_balance = balance_future.result()

            # Return the result after both functions complete
            return jsonify({
                'transactions': serialized_transactions,
                'total_transactions': total_transactions,
                'balance': serialized_balance
            }), 200

        except Exception as e:
            print(f'Error fetching transactions: {e}')
            # raise e;
            return jsonify({'error': 'An error occurred while fetching transactions'}), 500

    @staticmethod
    def get_balance(access_token):
        account_balance = AccountsBalanceGetRequest(access_token=access_token)
        balance = client.accounts_balance_get(account_balance)
        accounts = balance['accounts']
        serialized_balance = []
        for account in accounts:
            account_subtype = str(account.subtype)
            account_type = str(account.type)
            serialized_balance.append({
                'account_id': account.account_id,
                'mask': account.mask,
                'name': account.name,
                'official_name': account.official_name,
                'subtype': account_subtype,
                'type': account_type,
                'balances_available': account['balances']['available'],
                'balances_current': account['balances']['current'],

            })
        return serialized_balance

    @staticmethod
    def get_transactions(access_token, end_date, start_date):
        tran_request = TransactionsGetRequest(
            access_token=access_token,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
        )
        # Fetch transactions using Plaid's /transactions/get endpoint
        tran_response = client.transactions_get(
            tran_request
        )
        transactions = tran_response['transactions']
        serialized_transactions = []
        date_format = '%a, %d %b %Y %H:%M:%S %Z'

        for transaction in transactions:
            # Handle authorized_date: check if it's a string or already a date object
            authorized_date = transaction.authorized_date
            if isinstance(authorized_date, str):  # If it's a string, convert it
                authorized_date = datetime.strptime(authorized_date, date_format).date().isoformat()
            elif isinstance(authorized_date, (datetime, date)):  # If it's a datetime/date object
                authorized_date = authorized_date.isoformat()

            # Handle transaction date: check if it's a string or already a date object
            transaction_date = transaction.date
            if isinstance(transaction_date, str):  # If it's a string, convert it
                transaction_date = datetime.strptime(transaction_date, date_format).date().isoformat()
            elif isinstance(transaction_date, (datetime, date)):  # If it's a datetime/date object
                transaction_date = transaction_date.isoformat()

            serialized_transactions.append({
                'transaction_id': transaction.transaction_id,
                'name': transaction.name,
                'merchant_name': transaction.merchant_name,
                'authorized_date': authorized_date,
                'amount': transaction.amount,
                'date': transaction_date,
                'payment_channel': transaction.payment_channel,
                'account_id': transaction.account_id,
                'category': transaction.category,
                'website': transaction.website,
                'account_owner': transaction.account_owner,
                'pending': transaction.pending
            })
        return serialized_transactions, tran_response['total_transactions']
