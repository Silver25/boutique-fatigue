from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# in production to use s3 to store static files whenever someone runs
# collectstatic and that any uploaded product images to go there also
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
