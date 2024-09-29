from werkzeug.datastructures import FileStorage

from app.model.db.income_alchemy import LLCIncome
from app.service.azure_blob import AzureBlobStorage, BlobType
from app.util.date_util import DateUtil


class IncomeService:


    @staticmethod
    def save_income_form(income_form: LLCIncome, file: FileStorage):
        if file:
            file_path = DateUtil.prepend_timestamp_to_filename(file.filename)
            income_form.proof_of_income_file_path = file_path
            AzureBlobStorage.upload_file(file.read(), file_path, BlobType.INCOME_BLOB)
            income_form.save_income()
        else:
            income_form.save_income()
        return {'message': 'Income stored successfully'}, 200
