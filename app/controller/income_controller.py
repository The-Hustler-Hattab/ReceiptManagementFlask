from typing import Tuple, Dict

from flask import jsonify, Response, request
from werkzeug.datastructures import FileStorage

from app import Constants, app
from app.model.db.income_alchemy import LLCIncome
from app.service.income_service import IncomeService
from app.util.jwt_utls import verify_jwt, get_user_full_name

logger = app.logger
logger.name = 'IncomeController'


@app.route('/store-income', methods=['POST'])
# @verify_jwt
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
    if (tax + net_revenue) != gross_revenue:
        return {'message': 'tax + net_revenue != gross_revenue'}, 400
    llc_income: LLCIncome = LLCIncome()

    llc_income.source = source
    llc_income.gross_revenue = gross_revenue
    llc_income.net_revenue = net_revenue
    llc_income.tax = tax
    llc_income.comment = comment
    llc_income.created_by = get_user_full_name()

    logger.info(
        f"source: '{source}', gross_revenue: '{gross_revenue}', tax: '{tax}', comment: '{comment}',"
        f" net_revenue: '{net_revenue}, created_by: '{llc_income.created_by}', file: '{file.name}'")
    return IncomeService.save_income_form(llc_income, file)
