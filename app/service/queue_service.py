import base64

from azure.storage.queue import QueueServiceClient

from app import app, Constants


class QueueService:
    connection_string = app.config.get(Constants.BLOB_CONNECTION_STRING)
    queue_service_client = QueueServiceClient.from_connection_string(connection_string)
    queue_name = app.config.get(Constants.QUEUE_SHERIF_SALE)
    queue_client = queue_service_client.get_queue_client(queue_name)

    @staticmethod
    def push_message(message: str) -> None:

        # Encode the message in Base64
        encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')

        # Send the Base64 encoded message to the Azure Queue
        QueueService.queue_client.send_message(encoded_message)
        print(f"Message '{message}' (encoded as '{encoded_message}') pushed to Azure Queue Storage.")
