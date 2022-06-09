from typing import List, Any

from schema import Schema

from app.utils import exception
from botocore.exceptions import ClientError

from app.core.config import settings, logger

s3 = settings.s3_init()


def list_files(bucket_name):
    """List files in specific S3 URL"""
    response = s3.list_objects(Bucket=bucket_name)
    for content in response.get('Contents', []):
        yield content.get('Key')


def list_all_buckets():
    # Get all bucket names
    logger.info("listing all buckets")
    return [bucket.name for bucket in s3.buckets.all()]


class CRUDBucket:
    """
    This is a base class that will store and load data in an S3 Bucket
    Class attributes:
        - SCHEMA: a schema.Schema instance (https://github.com/keleshev/schema).
            This specify the structure of the data we store
        - name: A string that will define the folder on the S3 bucket
                in which we will store the file (this will allow for multiple models to be stored on the same bucket)
        """

    # By default: All dictionaries are valid
    SCHEMA = Schema(object)
    # The files will be stored in the raw folder
    name = 'raw'

    @classmethod
    def validate(cls, obj):
        return cls.SCHEMA.validate(obj)

    @classmethod
    def save(cls, bucket_name, file, filename) -> str:
        # We affect an id if there isn't one
        logger.info("saving file with name {0} in bucket: {1}", filename, bucket_name)
        cls.validate(file)
        obj = s3.Object(bucket_name, filename)
        obj.put(Body=file.file)
        return filename

    @classmethod
    def load(cls, bucket_name, file_name) -> (Any, str):
        bucket = s3.Bucket(bucket_name)
        if bucket.creation_date:
            for obj in bucket.objects.all():
                if file_name == obj.key:
                    file_content = obj.get()['Body'].read().decode('utf-8')
                    return file_content, None
                else:
                    logger.error("no file with name {0} in bucket: {1} exists", file_name, bucket_name)
                    raise exception.NoSuchFileExists('No such file exists')
        else:
            logger.error("no bucket with name {0} exists", bucket_name)
            raise exception.NoSuchBucketExists('No such bucket exists')
        return None, None

    @classmethod
    def delete_obj(cls, bucket_name, file):
        logger.info("deleting file with name {0} in bucket: {1}", file, bucket_name)
        return s3.Object(bucket_name, file).delete()

    @classmethod
    def create(cls, bucket_name, region):
        s3 = settings.s3_init(region)
        logger.info("creating bucket with name {1} in region {1}", bucket_name, region)
        try:
            location = {'LocationConstraint': region}
            bucket = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        except ClientError as e:
            raise e
        return bucket


    @classmethod
    def list_ids(cls, bucket_name) -> (Any, str):
        my_bucket = s3.Bucket(bucket_name)
        if my_bucket.creation_date:
            logger.info("listing all files in bucket {0}", bucket_name)
            return [bucket.key for bucket in my_bucket.objects.all()], None
        else:
            logger.error("no bucket with name {0} exists", bucket_name)
            raise exception.NoSuchBucketExists('No such bucket exists')
