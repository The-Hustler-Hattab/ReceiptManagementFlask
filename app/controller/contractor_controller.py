import io
import logging
from typing import Tuple, Dict

from flask import jsonify, Response, request, send_file
from werkzeug.datastructures import FileStorage

from app import app
from app.model.db.contractors_alchemy import Contractor
from app.service.azure_blob import AzureBlobStorage, BlobType
from app.service.contractor_service import ContractorService
from app.util.jwt_utls import verify_jwt, get_user_full_name, verify_token_and_role


log = logging.getLogger('ContractorController')


@app.route('/save-contractor', methods=['POST'])
@verify_jwt
def save_contractor() -> Tuple[Dict[str, str], int]:
    """
     Save Contractor Endpoint
     ---
     tags:
       - Contractor-Controller
     consumes:
       - multipart/form-data
     parameters:
       - name: file
         in: formData
         type: file
         required: false
         description: The file to upload.
       - name: contractor_name
         in: formData
         type: string
         required: true
         description: contractor name.
       - name: job_cost
         in: formData
         type: string
         required: true
         description: job_cost amount in dollars.
       - name: contractor_skills
         in: formData
         type: string
         required: true
         description: contractor skills.
       - name: comment
         in: formData
         type: string
         required: false
         description: comment.
       - name: phone_number
         in: formData
         type: string
         required: true
         description: phone number
     responses:
       200:
         description: OK if the file is uploaded successfully.
       400:
         description: Bad Request if no file is provided or the file format is invalid.
     """
    file = None
    if 'file' in request.files:
        file: FileStorage = request.files['file']

    contractor_name = request.form.get('contractor_name')
    job_cost = request.form.get('job_cost')
    contractor_skills = request.form.get('contractor_skills')
    phone_number = request.form.get('phone_number')
    comment = request.form.get('comment')


    contractor: Contractor = Contractor()

    contractor.contractor_name = contractor_name
    contractor.job_cost = job_cost
    contractor.contractor_skill = contractor_skills
    contractor.phone_number = phone_number
    contractor.comment = comment
    contractor.created_by = get_user_full_name()
    # contractor.created_by = 'TEST'

    log.info(
        f"contractor_name: '{contractor_name}', job_cost: '{job_cost}', phone_number: '{phone_number}', comment: '{comment}',"
        f" contractor_skills: '{contractor_skills}, created_by: '{contractor.created_by}'")

    return ContractorService.save_contractor_form(contractor, file)


@app.route('/get-all-contractors', methods=['GET'])
@verify_jwt
def get_all_contractors() -> Tuple[Dict[str, str], int]:
    """
    get list of contractors
    ---
    tags:
       - Contractor-Controller
    responses:
      200:
        description: OK if service gets all receipts.
    """
    try:
        # Fetch all contractors records and convert them to dictionaries
        contractors_records = Contractor.get_all()
        contractors_dicts = [contractor.to_dict() for contractor in contractors_records]  # Convert each record to a dictionary

        return {
            'contractors': contractors_dicts,
            'message': 'retrieved contractors successfully'
        }, 200
    except Exception as e:
        log.error(f"Error retrieving contractors: {e}")
        return {
            'message': 'Failed to retrieve contractors'
        }, 500


@app.route('/get-contractor-file', methods=['GET'])
@verify_jwt
def get_contractor_file():
    """
    Get file from Azure Blob Storage
    ---
    tags:
       - Contractor-Controller
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
            blob_data = AzureBlobStorage.download_file(blob_name, BlobType.CONTRACTOR_BLOB).readall()
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

@app.route('/delete-contractor', methods=['DELETE'])
@verify_token_and_role
def delete_contractor() -> tuple[Response, int]:
    """
    Delete a file from Azure Blob Storage
    ---
    tags:
       - Contractor-Controller
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
        if Contractor.delete_by_id(id):
            return jsonify({'message': f'deleted record \'{id}\' successfully'}), 200
        else:
            return jsonify({'message': f'record not found {id}'}), 404
    except Exception as e:
        return jsonify({'message': f'Failed to delete record \'{id}\': {e}'}), 500
