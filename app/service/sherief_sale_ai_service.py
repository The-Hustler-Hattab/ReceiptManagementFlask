from azure.core.polling import LROPoller

from app import Constants, app

from azure.ai.formrecognizer import DocumentAnalysisClient, AnalyzeResult

from azure.core.credentials import AzureKeyCredential

from app.model.db.sherif_sale_properties_alchemy import Property
from app.model.generic.sheriff_sale_detail_model import SheriffSaleDetailModel

endpoint = app.config.get(Constants.AZURE_FORM_RECOGNIZER_ENDPOINT)
key = app.config.get(Constants.AZURE_FORM_RECOGNIZER_KEY)
model_id = app.config.get(Constants.AZURE_FORM_RECOGNIZER_MODEL_ID)



document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)




class AzureCustomModel:
    @staticmethod
    def extract_sherif_sale_details( sheriff_sale_detail_model :SheriffSaleDetailModel) -> list[Property]:
        try:
            # Read the file content as bytes
            # Convert bytes to base64 string
            poller: LROPoller[AnalyzeResult] = document_analysis_client.begin_analyze_document_from_url(model_id, f"https://receiptsllc.blob.core.windows.net/sherifsale/{sheriff_sale_detail_model.file_path}")



            property_list: list[Property] = []
            result = poller.result().documents[0].fields.get("property").value


            print(str(result))
            for item in result:
                property = Property()
                property.sale = item.value.get("Sale").value[:254]  if item.value.get("Sale") and item.value.get("Sale").value else ""
                property.case_number = item.value.get("caseNum").value[:254] if item.value.get("caseNum") and item.value.get("caseNum").value else ""
                property.sale_type = item.value.get("SaleType").value[:254] if item.value.get("SaleType") and item.value.get("SaleType").value else ""
                property.status = item.value.get("Status").value[:254] if item.value.get("Status") and item.value.get("Status").value else ""
                property.tracts = item.value.get("Tracts").value[:254] if item.value.get("Tracts") and item.value.get("Tracts").value else ""
                property.cost_tax_bid = item.value.get("CostTaxBid").value[:254] if item.value.get("CostTaxBid") and item.value.get("CostTaxBid").value else ""
                property.plaintiff = item.value.get("Plantiff").value[:254] if item.value.get("Plantiff") and item.value.get("Plantiff").value else ""
                property.attorney_for_plaintiff = item.value.get("AttorneyForPlantiff").value[:254] if item.value.get("AttorneyForPlantiff") and item.value.get("AttorneyForPlantiff").value else ""
                property.defendant = item.value.get("Defendents").value[:254].replace("\n", " ") if item.value.get("Defendents") and item.value.get("Defendents").value else ""
                property.property_address = item.value.get("PropertyAddress").value[:254].replace("\n", " ") if item.value.get("PropertyAddress") and item.value.get("PropertyAddress").value else ""
                property.municipality = item.value.get("Municipality").value[:254] if item.value.get("Municipality") and item.value.get("Municipality").value else ""
                property.parcel_tax_id = item.value.get("ParcelTaxId").value[:254] if item.value.get("ParcelTaxId") and item.value.get("ParcelTaxId").value else ""
                property.comments = item.value.get("Comments").value[:254] if item.value.get("Comments") and item.value.get("Comments").value else ""
                property.SHERIEF_SALE_CHILD_ID = sheriff_sale_detail_model.sheriff_sale_child_id
                if property.tracts == "1":
                    address = property.property_address.replace(" ", "-")
                    zillow_link = f"https://www.zillow.com/homes/{address}_rb/"
                    property.zillow_link = zillow_link

                property_list.append(property)
            return property_list
        except Exception as e:
            print(e)
            raise e
