#
#
# import plaid
# from plaid.api import plaid_api
# from plaid.model.transactions_sync_request import TransactionsSyncRequest
# from flask import jsonify, Response, request
# from app import Constants, app
#
# configuration = plaid.Configuration(
#     host=plaid.Environment.Sandbox,
#     api_key={
#         'clientId': app.config.get(Constants.PLAID_CLIENT_ID),
#         'secret': app.config.get(Constants.PLAID_SECRET),
#     }
# )
#
# api_client = plaid.ApiClient(configuration)
# client = plaid_api.PlaidApi(api_client)
#
# @app.route('/get-transactions', methods=['GET'])
# def get_transactions():
#     """
#     Get list of transactions from Plaid
#     ---
#     tags:
#       - PLAID-Controller
#     parameters:
#       - name: access_token
#         in: query
#         type: string
#         required: true
#         description: Plaid access token for pulling transactions
#     responses:
#       200:
#         description: List of transactions retrieved successfully
#       500:
#         description: Internal server error
#     """
#     try:
#         # Extract access token from the query parameters
#         access_token = request.args.get('access_token')
#         print(access_token)
#         # Check if access_token is provided
#         if not access_token:
#             return jsonify({"error": "Missing access_token"}), 400
#
#         # Create the request object for Plaid's transactions_sync
#         sync_request = TransactionsSyncRequest(access_token=access_token)
#
#         # First call to Plaid API to sync transactions
#         response = client.transactions_sync(sync_request)
#         transactions = response['added']
#
#         # Continue fetching transactions if there are more
#         while response.get('has_more', False):
#             sync_request = TransactionsSyncRequest(
#                 access_token=access_token,
#                 cursor=response['next_cursor']
#             )
#             response = client.transactions_sync(sync_request)
#             transactions += response['added']
#
#         # Return the list of transactions
#         return jsonify(transactions), 200
#
#     except Exception as e:
#         print(f"Error fetching transactions: {str(e)}")
#         return jsonify({"error": "Internal server error"}), 500