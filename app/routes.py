import io
from datetime import datetime, timedelta
from typing import Tuple, Dict

from flask import jsonify, Response, request, send_file

from app import app, Constants, verify_jwt
from app.model.db.receipts_alchemy import Receipts, Receipt
from app.service.analytics import AnalyticsService
from app.service.azure_blob import AzureBlobStorage
from app.service.process_receipts import AzureFormRecognizer


@app.route('/health', methods=['GET'])
def health() -> Tuple[Dict[str, str], int]:
    """
    Health Check Endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: OK if the service is healthy.
    """
    return {'status': 'OK',
            'msg': 'API is up'}, 200


@verify_jwt
@app.route('/get-list-of-receipts', methods=['GET'])
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


@verify_jwt
@app.route('/process-receipts/<company_name>/<customer_name>', methods=['POST'])
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
        # For demonstration, we'll just return a JSON message
        return AzureFormRecognizer.process_receipts(pdf_file.read(), company_name, customer_name)
    else:
        return {'message': 'Invalid file format. Only PDF files are allowed'}, 404


@verify_jwt
@app.route('/store-receipts-ai-assisted', methods=['POST'])
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
        receipt.created_by = Constants.APP_NAME
        receipt.created_at = datetime.now()
        # Process the PDF file
        # For demonstration, we'll just return a JSON message
        return AzureFormRecognizer.store_receipt_ai_assisted(pdf_file.read(), receipt)
    else:
        return {'message': 'Invalid file format. Only PDF files are allowed'}, 404


@verify_jwt
@app.route('/process-receipts-ai-assisted', methods=['POST'])
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


@verify_jwt
@app.route('/delete-file-by-path', methods=['DELETE'])
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


@verify_jwt
@app.route('/get-file')
def get_file():
    """
    Get file from Azure Blob Storage
    ---
    tags:
      - Blob-Controller
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
            blob_data = AzureBlobStorage.download_file(blob_name).readall()
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


@verify_jwt
@app.route('/get-list-of-files', methods=['GET'])
def get_files():
    """
    Get list of files from Azure Blob Storage
    ---
    tags:
      - Blob-Controller
    responses:
      200:
        description: List of files retrieved successfully
      500:
        description: Internal server error
    """
    try:
        files = AzureBlobStorage.list_files()
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@verify_jwt
@app.route('/delete-file', methods=['DELETE'])
def delete_file() -> tuple[Response, int]:
    """
    Delete a file from Azure Blob Storage
    ---
    tags:
      - Blob-Controller
    parameters:
      - name: blob_name
        in: query
        type: string
        required: true
        description: The name of the file to delete
    responses:
      200:
        description: File deleted successfully
      400:
        description: Bad request - blob_name parameter is missing
      500:
        description: Internal server error
    """
    blob_name = request.args.get('blob_name')
    print(blob_name)
    if not blob_name:
        return jsonify({'message': 'blob_name parameter is required'}), 400

    return AzureBlobStorage.delete_file(blob_name)


@app.route('/get-bar-chart-data', methods=['GET'])
@verify_jwt
def get_bar_chart_data():
    """
    Get bar chart data
    ---
    tags:
      - Analytics-Controller
    parameters:
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD

    responses:
      200:
        description: bar chart data retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date)
    print(end_date)

    try:
        # Parse the date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the start_date to the first day of the month
        start_date = start_date.replace(day=1)

        # Set the end_date to the last day of the month
        end_date = end_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        print(start_date)
        print(end_date)
        return AnalyticsService.get_bar_chart_data(start_date, end_date)
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500


@verify_jwt
@app.route('/get-pie-chart-data', methods=['GET'])
def get_pie_chart_data():
    """
    Get pie chart data
    ---
    tags:
      - Analytics-Controller
    parameters:
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD

    responses:
      200:
        description: bar chart data retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date)
    print(end_date)

    try:
        # Parse the date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the start_date to the first day of the month
        start_date = start_date.replace(day=1)

        # Set the end_date to the last day of the month
        end_date = end_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        print(start_date)
        print(end_date)
        return AnalyticsService.get_pie_chart_data(start_date, end_date)
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500


@verify_jwt
@app.route('/get-line-chart-data', methods=['GET'])
def get_line_chart_data():
    """
    Get line chart data
    ---
    tags:
      - Analytics-Controller
    parameters:
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD

    responses:
      200:
        description: line chart data retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date)
    print(end_date)

    try:
        # Parse the date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the start_date to the first day of the month
        start_date = start_date.replace(day=1)

        # Set the end_date to the last day of the month
        end_date = end_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        print(start_date)
        print(end_date)
        return AnalyticsService.get_line_chart_data(start_date, end_date)
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500


@verify_jwt
@app.route('/get-horizontal-chart-data', methods=['GET'])
def get_horizontal_chart_data():
    """
    Get horizontal chart data
    ---
    tags:
      - Analytics-Controller
    parameters:
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD

    responses:
      200:
        description: horizontal chart data retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date)
    print(end_date)

    try:
        # Parse the date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the start_date to the first day of the month
        start_date = start_date.replace(day=1)

        # Set the end_date to the last day of the month
        end_date = end_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        print(start_date)
        print(end_date)
        return AnalyticsService.get_horizontal_chart_data(start_date, end_date)
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500
