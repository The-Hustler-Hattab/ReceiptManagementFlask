import io
from datetime import datetime, timedelta
from typing import Tuple, Dict

from flask import jsonify, Response, request, send_file

from app import app, oauth, verify_jwt
from app.model.receipts_alchemy import Receipts
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



