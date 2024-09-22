from datetime import datetime, timedelta
from typing import Tuple, Dict, IO

from flask import jsonify, Response, request
from werkzeug.datastructures import FileStorage

from app import app, Constants
from app.service.sherief_sale_service import SheriffSaleService
from app.util.date_util import DateUtil
from app.util.jwt_utls import verify_jwt


@app.route('/process-sherif-sale-master-pdf', methods=['POST'])
@verify_jwt
def process_sherif_sale_master_pdf() -> Tuple[Dict[str, str], int]:
    """
     Process Sherif sale PDF Endpoint
     ---
     tags:
       - Sherif-Controller
     consumes:
       - multipart/form-data
     parameters:
       - name: file
         in: formData
         type: file
         required: true
         description: The PDF file to upload.
       - name: sherif_sale_date
         in: formData
         type: string
         required: true
         description: sale date in the format YYYY-MM-DD

     responses:
       200:
         description: OK if the file is processed successfully.
       400:
         description: Bad Request if no file is provided or the file format is invalid or date is invalid.
     """
    # Check if the request contains a file
    if 'file' not in request.files:
        return {'message': 'No file provided'}, 400

    pdf_file: FileStorage = request.files['file']
    filename = pdf_file.filename.lower()
    # Access the sherif_sale_date
    sherif_sale_date: str = request.form.get('sherif_sale_date')

    if not sherif_sale_date:
        return {"message": "Sherif sale date is required"}, 400
    # Process the PDF file and sherif_sale_date as needed
    # For example, parse the date and validate it
    try:
        # Convert the sherif_sale_date to a datetime object if needed
        DateUtil.convert_string_to_date(sherif_sale_date)
    except ValueError:
        return {"message": "Invalid date format, expected YYYY-MM-DD"}, 400

    # Check if the file is a PDF
    if filename.endswith('.pdf'):
        return SheriffSaleService.process_master_pdf(pdf_file, sherif_sale_date)
    else:
        return {'message': 'Invalid file format. Only PDF files are allowed'}, 400


@app.route('/enrich-sherif-sale', methods=['POST'])
@verify_jwt
def enrich_sherif_sale() -> Tuple[Dict[str, str], int]:
    """
     Enrich Sherif sale PDF Endpoint
     ---
     tags:
       - Sherif-Controller

     responses:
       200:
         description: OK enriched successfully.
       400:
         description: Bad Request there was an error enriching data.
     """

    return SheriffSaleService.enrich_sherif_sale();


@app.route('/sheriff-sale-data-between', methods=['GET'])
@verify_jwt
def get_sheriff_data_between():
    """
    Get sheriff data between two dates
    ---
    tags:
      - Sherif-Controller
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
        description: data pulled successfully
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

        print(start_date)
        print(end_date)

        return SheriffSaleService.get_sheriff_sale_data_between_two_dates(start_date, end_date)
    except Exception as e:
        raise e