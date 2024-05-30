import io
from datetime import datetime, timedelta
from typing import Tuple, Dict

from flask import jsonify, Response, request, send_file

from app import app
from app.service.azure_blob import AzureBlobStorage
from app.util.jwt_utls import verify_jwt, verify_token_and_role


@app.route('/get-file')
@verify_jwt
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
@verify_jwt
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
@verify_token_and_role
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


@app.route('/files-between', methods=['GET'])
@verify_jwt
def get_files_between():
    """
    Get files between two dates as zip file
    ---
    tags:
      - Blob-Controller
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
        description: bar zip files successfully
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
        # return AzureBlobStorage.get_files_between_dates(start_date, end_date)
        return send_file(
            io.BytesIO(AzureBlobStorage.get_files_between_dates(start_date, end_date)),
            as_attachment=True,
            download_name='Receipts.zip'
        )
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500

@app.route('/update-file-hashes', methods=['POST'])
@verify_jwt
def update_file_hashes() -> tuple[Response, int]:
    """
     update file hashes Endpoint
     ---
     tags:
       - Receipts-Controller
     responses:
       200:
         description: OK if the file hashes updated successfully.
       400:
         description: Bad Request if no file is provided or the format is invalid.
     """

    return AzureBlobStorage.update_files_hash_in_table()