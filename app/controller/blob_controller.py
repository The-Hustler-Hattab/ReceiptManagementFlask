import io

from flask import jsonify, Response, request, send_file

from app import app,  verify_jwt
from app.service.azure_blob import AzureBlobStorage

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
@verify_jwt
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