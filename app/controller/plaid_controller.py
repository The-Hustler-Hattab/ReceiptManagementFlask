import logging
from typing import Tuple, Dict

from flask import jsonify, Response, request
from app import Constants, app, client
from app.model.db.plaid_access_token_alchemy import PlaidInstitutionAccessTokens
from app.service.plaid_service import PlaidService

from app.util.jwt_utls import get_user_email, verify_jwt, verify_token_and_role

log = logging.getLogger('PlaidController')


@app.route('/get-transactions', methods=['GET'])
@verify_token_and_role
def get_transactions():
    """
    Fetch transactions for a specific account ID
    ---
    tags:
      - PLAID-Controller
    parameters:
      - in: query
        name: bank_id
        description: The id for the bank account
        required: true
        schema:
          type: string
      - in: query
        name: start_date
        description: Start date for transactions in 'YYYY-MM-DD' format
        required: true
        schema:
          type: string
      - in: query
        name: end_date
        description: End date for transactions in 'YYYY-MM-DD' format
        required: true
        schema:
          type: string
    responses:
      200:
        description: Transactions retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    # Extract query parameters
    bank_id = int( request.args.get('bank_id'))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Check if bank_id is provided
    if not bank_id:
        return jsonify({"message": "bank_id is required"}), 400
    if not start_date:
        return jsonify({"message": "start_date is required"}), 400
    if not end_date:
        return jsonify({"message": "end_date is required"}), 400

    # Example: Logic to fetch transactions based on these parameters
    try:
        # Call your service or logic to retrieve transactions here
        return PlaidService.get_transactions_and_balance(bank_id, start_date, end_date)

    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 500
@app.route('/create-link-token', methods=['POST'])
@verify_token_and_role
def create_link_token():
    """
    Create a link token for Plaid
    ---
    tags:
      - PLAID-Controller
    responses:
      200:
        description: Link token created successfully
      500:
        description: Internal server error
    """
    return PlaidService.create_link_token()



@app.route('/exchange-public-token', methods=['POST'])
@verify_token_and_role
def exchange_public_token():
    """
    Exchange the public token for an access token and save account details
    ---
    tags:
      - PLAID-Controller
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: JSON body containing the public token, institution ID, institution name, and accounts
        required: true
        schema:
          type: object
          required:
            - public_token
            - institution_id
            - institution_name
            - accounts
          properties:
            public_token:
              type: string
              description: Plaid public token generated from Plaid Link
            institution_id:
              type: string
              description: The ID of the financial institution
            institution_name:
              type: string
              description: The name of the financial institution
            accounts:
              type: array
              description: List of accounts associated with the institution
              items:
                type: object
                required:
                  - id
                  - mask
                  - name
                  - subtype
                  - type
                properties:
                  id:
                    type: string
                    description: The unique identifier of the account
                  mask:
                    type: string
                    description: Last 4 digits of the account number
                  name:
                    type: string
                    description: The name of the account
                  subtype:
                    type: string
                    description: The subtype of the account (e.g., checking, savings)
                  type:
                    type: string
                    description: The type of the account (e.g., depository, credit)
    responses:
      200:
        description: Access token and accounts saved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    data = request.get_json()

    return PlaidService.create_access_token(data)

@app.route('/get-all-banks', methods=['GET'])
@verify_token_and_role
def get_all_banks() -> Tuple[Dict[str, str], int]:
    """
    get list of income
    ---
    tags:
      - PLAID-Controller
    responses:
      200:
        description: OK if service gets all receipts.
    """
    try:
        # Fetch all income records and convert them to dictionaries
        banks_records = PlaidInstitutionAccessTokens.get_all()
        bank_dicts = [bank.to_dict() for bank in banks_records]  # Convert each record to a dictionary

        return {
            'banks': bank_dicts,
            'message': 'retrieved income successfully'
        }, 200
    except Exception as e:
        log.error(f"Error retrieving income: {e}")
        # raise e
        return {
            'message': 'Failed to retrieve income'
        }, 500