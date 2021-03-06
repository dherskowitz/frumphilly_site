# from storages.backends.azure_storage import AzureStorage
from storages.backends.s3boto3 import S3Boto3Storage

# from django.conf import settings

# from decouple import config


class S3StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class S3SiteImagesStorage(S3Boto3Storage):
    location = "media/images"
    default_acl = "public-read"


class S3UserAccountStorage(S3Boto3Storage):
    location = "media/accounts"
    file_overwrite = False
    default_acl = None


class S3EventsMediaStorage(S3Boto3Storage):
    location = "media/events/images"
    file_overwrite = False
    default_acl = None


class S3EventsFileStorage(S3Boto3Storage):
    location = "media/events/files"
    file_overwrite = False
    default_acl = None


class S3ListingsMediaStorage(S3Boto3Storage):
    location = "media/listings/images"
    file_overwrite = False
    default_acl = None


class S3AdsMediaStorage(S3Boto3Storage):
    location = "media/ads/images"
    file_overwrite = False
    default_acl = None


# class AzureMediaStorage(AzureStorage):
#     account_name = config("AZURE_ACCOUNT_NAME")
#     account_key = config("AZURE_ACCOUNT_KEY")
#     azure_container = config("AZURE_MEDIA_CONTAINER")
#     expiration_secs = None


# class AzureStaticStorage(AzureStorage):
#     account_name = config("AZURE_ACCOUNT_NAME")
#     account_key = config("AZURE_ACCOUNT_KEY")
#     azure_container = config("AZURE_ASSETS_CONTAINER")
#     expiration_secs = None


# # Storage for Event Images
# class EventMediaStorage(AzureStorage):
#     account_name = config("AZURE_ACCOUNT_NAME")
#     account_key = config("AZURE_ACCOUNT_KEY")
#     azure_container = f'{config("AZURE_MEDIA_CONTAINER")}/events/images'
#     expiration_secs = None


# # Storage for Event Attachments / Files
# class EventFileStorage(AzureStorage):
#     account_name = config("AZURE_ACCOUNT_NAME")
#     account_key = config("AZURE_ACCOUNT_KEY")
#     azure_container = f'{config("AZURE_MEDIA_CONTAINER")}/events/files'
#     expiration_secs = None
