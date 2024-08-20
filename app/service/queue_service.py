# from azure.storage.queue import QueueServiceClient
#
# from app import app, Constants
#
#
# class QueueService:
#     connection_string = app.config.get(Constants.BLOB_CONNECTION_STRING)
#     queue_service_client = QueueServiceClient.from_connection_string(connection_string)
#     queue_name = app.config.get(Constants.QUEUE_SHERIF_SALE)
#     queue_client = queue_service_client.get_queue_client(queue_name)
#
#     @staticmethod
#     def push_message(message: str) -> None:
#         QueueService.queue_client.send_message(message)
#         print(f"Message '{message}' pushed to Azure Queue Storage.")
