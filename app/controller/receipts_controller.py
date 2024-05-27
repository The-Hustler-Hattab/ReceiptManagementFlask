from datetime import datetime
from typing import Tuple, Dict

from flask import jsonify, Response, request

from app import app, Constants
from app.model.db.receipts_alchemy import Receipts, Receipt
from app.service.process_receipts import AzureFormRecognizer
from app.util.jwt_utls import verify_jwt, verify_token_and_role, get_decoded_token, get_full_name


@app.route('/get-list-of-receipts', methods=['GET'])
@verify_jwt
def get_list_of_receipts() -> Tuple[Dict[str, str], int]:
    """
    get list of receipts
    ---
    tags:
      - Receipts-Controller
    responses:
      200:
        description: OK if service gets all receipts.
    """
    return {'receipts': Receipts.convert_receipts_to_dicts(Receipts.get_all()),
            'msg': 'retrieved receipts successfully'}, 200


@app.route('/process-receipts/<company_name>/<customer_name>', methods=['POST'])
@verify_jwt
def process_receipts(company_name: str, customer_name: str) -> Tuple[Dict[str, str], int]:
    """
     Process PDF receipts Endpoint
     ---
     tags:
       - Receipts-Controller
     consumes:
       - multipart/form-data
     parameters:
       - name: file
         in: formData
         type: file
         required: true
         description: The PDF file to upload.
       - name: company_name
         in: path
         type: string
         required: true
         description: The name of the company which made the purchase.
       - name: customer_name
         in: path
         type: string
         required: true
         description: The name of the customer which made the purchase.
     responses:
       200:
         description: OK if the file is uploaded successfully.
       400:
         description: Bad Request if no file is provided or the file format is invalid.
     """
    # Check if the request contains a file
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 404

    pdf_file = request.files['file']
    print(company_name)
    print(customer_name)

    # Check if the file is a PDF
    if pdf_file.filename.endswith('.pdf'):
        # Process the PDF file
        created_by = get_full_name()
        return AzureFormRecognizer.process_receipts(pdf_file.read(), company_name, customer_name, created_by)
    else:
        return {'message': 'Invalid file format. Only PDF files are allowed'}, 404


@app.route('/store-receipts-ai-assisted', methods=['POST'])
@verify_jwt
def store_receipts_ai_assisted() -> Tuple[Dict[str, str], int]:
    """
     Process PDF receipts with AI assistance Endpoint
     ---
     tags:
       - Receipts-Controller
     consumes:
       - multipart/form-data
     parameters:
       - name: file
         in: formData
         type: file
         required: true
         description: The PDF file to upload.
       - name: total
         in: formData
         type: number
         required: true
         description: The total amount.
       - name: sub_total
         in: formData
         type: number
         required: true
         description: The sub total amount.
       - name: tax
         in: formData
         type: number
         required: true
         description: The tax amount.
       - name: company_name
         in: formData
         type: string
         required: true
         description: The name of the company.
       - name: vendor
         in: formData
         type: string
         required: true
         description: The vendor's name.
       - name: purchased_at
         in: formData
         type: string
         format: date
         required: true
         description: The purchase date.
       - name: vendor_address
         in: formData
         type: string
         required: false
         description: The vendor's address.
       - name: customer_name
         in: formData
         type: string
         required: true
         description: The customer's name.
       - name: invoice_id
         in: formData
         type: string
         required: false
         description: The invoice ID.
     responses:
       200:
         description: OK if the file is uploaded successfully.
       400:
         description: Bad Request if no file is provided or the file format is invalid.
     """
    # Check if the request contains a file
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 404

    pdf_file = request.files['file']
    print(pdf_file)
    # Check if the file is a PDF
    if pdf_file.filename.endswith('.pdf'):
        total = request.form.get('total')
        sub_total = request.form.get('sub_total')
        tax = request.form.get('tax')
        company_name = request.form.get('company_name')
        vendor = request.form.get('vendor')
        purchased_at = request.form.get('purchased_at')
        vendor_address = request.form.get('vendor_address')
        customer_name = request.form.get('customer_name')
        invoice_id = request.form.get('invoice_id')

        receipt: Receipt = Receipt.empty()
        receipt.total = float(total)
        receipt.sub_total = float(sub_total)
        receipt.tax = float(tax)
        receipt.company_name = company_name
        receipt.vendor = vendor
        receipt.purchased_at = datetime.strptime(purchased_at, "%Y-%m-%d").date()
        receipt.vendor_address = vendor_address
        receipt.customer_name = customer_name
        receipt.invoice_id = invoice_id

        full_name = get_full_name()
        print(full_name)
        if full_name:
            receipt.created_by = full_name
        else:
            receipt.created_by = Constants.APP_NAME

        receipt.created_at = datetime.now()
        # Process the PDF file
        # For demonstration, we'll just return a JSON message
        return AzureFormRecognizer.store_receipt_ai_assisted(pdf_file.read(), receipt)
    else:
        return {'message': 'Invalid file format. Only PDF files are allowed'}, 404


@app.route('/process-receipts-ai-assisted', methods=['POST'])
@verify_jwt
def process_receipts_ai_assisted() -> Tuple[Dict[str, str], int]:
    """
     process PDF receipts with ai assistance Endpoint
     ---
     tags:
       - Receipts-Controller
     consumes:
       - multipart/form-data
     parameters:
       - name: file
         in: formData
         type: file
         required: true
         description: The PDF file to upload.

     responses:
       200:
         description: OK if the file is uploaded successfully.
       400:
         description: Bad Request if no file is provided or the file format is invalid.
     """
    # Check if the request contains a file
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 404

    pdf_file = request.files['file']
    print(pdf_file)
    # Check if the file is a PDF
    if pdf_file.filename.endswith('.pdf'):
        # Process the PDF file
        # For demonstration, we'll just return a JSON message
        return AzureFormRecognizer.process_receipts_ai_assisted(pdf_file.read())
    else:
        return {'message': 'Invalid file format. Only PDF files are allowed'}, 404


@app.route('/delete-file-by-path', methods=['DELETE'])
@verify_token_and_role
def delete_file_by_file_path() -> tuple[Response, int]:
    """
    Delete a file from table by file_path
    ---
    tags:
      - Receipts-Controller
    parameters:
      - name: file_path
        in: query
        type: string
        required: true
        description: The name of the file to delete
    responses:
      200:
        description: File deleted successfully
      400:
        description: Bad request - file_path parameter is missing
      500:
        description: Internal server error
    """
    file_path = request.args.get('file_path')
    print(file_path)
    if not file_path:
        return jsonify({'message': 'file_path parameter is required'}), 400

    return Receipts.delete_by_file_path(file_path)
