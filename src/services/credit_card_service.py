from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.Config import Config

def analize_credit_card(card_url):
    try:
        credential = AzureKeyCredential(Config.KEY)
        document_Client = DocumentIntelligenceClient(Config.ENDPOINT, credential)

        poller = document_Client.begin_analyze_document(
            model_id="prebuilt-creditCard",
            body=AnalyzeDocumentRequest(url_source=card_url)
        )
        result = poller.result()

        if not result.documents:
            return {"error": "Nenhum documento foi detectado."}

        document = result.documents[0]
        fields = document.fields

        def get_field_content(field_name):
            field = fields.get(field_name)
            return field.content if field else None

        return {
            "card_name": get_field_content("CardHolderName"),
            "card_number": get_field_content("CardNumber"),
            "expiry_date": get_field_content("ExpirationDate"),
            "bank_name": get_field_content("IssuingBank"),
        }

    except Exception as e:
        return {"error": f"Erro ao analisar o cartão: {e}"}
        

