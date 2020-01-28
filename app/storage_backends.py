from storages.backends.azure_storage import AzureStorage
from decouple import config


class AzureMediaStorage(AzureStorage):
    account_name = config("AZURE_ACCOUNT_NAME")
    account_key = config("AZURE_ACCOUNT_KEY")
    azure_container = config("AZURE_MEDIA_CONTAINER")
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = config("AZURE_ACCOUNT_NAME")
    account_key = config("AZURE_ACCOUNT_KEY")
    azure_container = config("AZURE_ASSETS_CONTAINER")
    expiration_secs = None


# Storage for Event Images
class EventMediaStorage(AzureStorage):
    account_name = config("AZURE_ACCOUNT_NAME")
    account_key = config("AZURE_ACCOUNT_KEY")
    azure_container = f'{config("AZURE_MEDIA_CONTAINER")}/events/images'
    expiration_secs = None


# Storage for Event Attachments / Files
class EventFileStorage(AzureStorage):
    account_name = config("AZURE_ACCOUNT_NAME")
    account_key = config("AZURE_ACCOUNT_KEY")
    azure_container = config("AZURE_ASSETS_CONTAINER")
    expiration_secs = None
