import io
import logging
from datetime import datetime
from typing import Tuple, Dict

from flask import jsonify, Response, request, send_file
from werkzeug.datastructures import FileStorage

from app import Constants, app
from app.model.db.income_alchemy import LLCIncome
from app.service.azure_blob import AzureBlobStorage, BlobType
from app.service.income_service import IncomeService
from app.util.date_util import DateUtil
from app.util.jwt_utls import verify_jwt, get_user_full_name, verify_token_and_role


log = logging.getLogger('IncomeController')


@app.route('/store-income', methods=['POST'])
@verify_jwt
def store_income() -> Tuple[Dict[str, str], int]:
    """
     Store Income Endpoint
     ---
     tags:
       - Income-Controller
     consumes:
       - multipart/form-data
     parameters:
       - name: file
         in: formData
         type: file
         required: false
         description: The PDF file to upload.
       - name: source
         in: formData
         type: string
         required: true
         description: source of the income.
       - name: gross_revenue
         in: formData
         type: string
         required: true
         description: income amount in dollars.
       - name: net_revenue
         in: formData
         type: string
         required: true
         description: income amount after tax in dollars.
       - name: tax
         in: formData
         type: string
         required: true
         description: The tax amount.
       - name: comment
         in: formData
         type: string
         required: false
         description: comment on the income.
       - name: received_at
         in: formData
         type: string
         required: false
         description: date income received.
     responses:
       200:
         description: OK if the file is uploaded successfully.
       400:
         description: Bad Request if no file is provided or the file format is invalid.
     """
    file = None
    if 'file' in request.files:
        file: FileStorage = request.files['file']

    source = request.form.get('source')
    gross_revenue = float(request.form.get('gross_revenue'))
    net_revenue = float(request.form.get('net_revenue'))
    tax = float(request.form.get('tax'))
    comment = request.form.get('comment')
    received_at = request.form.get('received_at')
    received_at_date: datetime = DateUtil.convert_string_to_date(received_at)

    if (tax + net_revenue) != gross_revenue:
        return {'message': 'tax + net_revenue != gross_revenue'}, 400
    llc_income: LLCIncome = LLCIncome()

    llc_income.source = source
    llc_income.gross_revenue = gross_revenue
    llc_income.net_revenue = net_revenue
    llc_income.tax = tax
    llc_income.comment = comment
    llc_income.created_by = get_user_full_name()
    llc_income.received_at = received_at_date
    log.info(
        f"source: '{source}', gross_revenue: '{gross_revenue}', tax: '{tax}', comment: '{comment}',"
        f" net_revenue: '{net_revenue}, created_by: '{llc_income.created_by}'")
    return IncomeService.save_income_form(llc_income, file)


@app.route('/get-all-income', methods=['GET'])
@verify_jwt
def get_all_income() -> Tuple[Dict[str, str], int]:
    """
    get list of income
    ---
    tags:
      - Income-Controller
    responses:
      200:
        description: OK if service gets all receipts.
    """
    try:
        # Fetch all income records and convert them to dictionaries
        income_records = LLCIncome.get_all()
        income_dicts = [income.to_dict() for income in income_records]  # Convert each record to a dictionary

        return {
            'income': income_dicts,
            'message': 'retrieved income successfully'
        }, 200
    except Exception as e:
        log.error(f"Error retrieving income: {e}")
        return {
            'message': 'Failed to retrieve income'
        }, 500


@app.route('/get-income-file', methods=['GET'])
@verify_jwt
def get_income_file():
    """
    Get file from Azure Blob Storage
    ---
    tags:
      - Income-Controller
    parameters:
      - name: path
        in: query
        type: string
        required: true
        description: Path of the file in Azure Blob Storage
    responses:
      200:
        description: File retrieved successfully
      400:
        description: Path parameter is missing
      404:
        description: File not found
    """
    blob_name = request.args.get('path')
    print(blob_name)
    if blob_name:
        try:

            # Download the blob data
            blob_data = AzureBlobStorage.download_file(blob_name, BlobType.INCOME_BLOB).readall()
            # Return the blob data as a file attachment
            return send_file(
                io.BytesIO(blob_data),
                as_attachment=True,
                download_name=blob_name
            )
        except Exception as e:
            return str(e), 404
    else:
        return "Path parameter is missing", 400

@app.route('/delete-income', methods=['DELETE'])
@verify_token_and_role
def delete_income() -> tuple[Response, int]:
    """
    Delete a file from Azure Blob Storage
    ---
    tags:
      - Income-Controller
    parameters:
      - name: id
        in: query
        type: string
        required: true
        description: id of the income record
    responses:
      200:
        description: record deleted successfully
      400:
        description: Bad request - id parameter is missing
      500:
        description: Internal server error
    """
    id =  request.args.get('id')
    try:
        if not id:
            return jsonify({'message': 'id parameter is required'}), 400
        if LLCIncome.delete_by_id(id):
            return jsonify({'message': f'deleted record \'{id}\' successfully'}), 200
        else:
            return jsonify({'message': f'record not found {id}'}), 404
    except Exception as e:
        return jsonify({'message': f'Failed to delete record \'{id}\': {e}'}), 500
