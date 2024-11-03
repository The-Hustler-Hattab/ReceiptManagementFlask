from werkzeug.datastructures import FileStorage

from app.model.db.contractors_alchemy import Contractor
from app.service.azure_blob import AzureBlobStorage, BlobType
from app.util.date_util import DateUtil


class ContractorService:


    @staticmethod
    def save_contractor_form(contractor_form: Contractor, file: FileStorage):
        if file:
            file_path = DateUtil.prepend_timestamp_to_filename(file.filename)
            AzureBlobStorage.upload_file(file.read(), file_path, BlobType.CONTRACTOR_BLOB)
            contractor_form.quote_file_location = file_path

            contractor_form.save_contractor()
        else:
            contractor_form.save_contractor()
        return {'message': 'Contractor stored successfully'}, 200
