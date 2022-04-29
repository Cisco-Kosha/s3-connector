from typing import List, Any

import json
import boto3
import os
import uuid
from schema import Schema

from app.core.config import settings

s3 = settings.s3_init()


def list_files(bucket_name):
    """List files in specific S3 URL"""
    response = s3.list_objects(Bucket=bucket_name)
    for content in response.get('Contents', []):
        yield content.get('Key')


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
    def save(cls, bucket_name, obj, filename) -> str:
        # We affect an id if there isn't one
        obj = cls.validate(obj)
        s3.put_object(
            Bucket=bucket_name,
            Body=obj.file,
            Key=filename
        )
        return filename

    @classmethod
    def load(cls, bucket_name, file_name):
        obj = s3.get_object(
            Bucket=bucket_name,
            Key=file_name,
        )
        obj = obj['Body'].read().decode('utf-8')
        return obj

    @classmethod
    def delete_obj(cls, bucket_name, file):
        s3.delete_object(
            Bucket=bucket_name,
            Key=file,
        )
        return {'deleted_id': file}

    @classmethod
    def list_ids(cls, bucket_name):
        file_names = []
        file_list = list_files(bucket_name)
        for file in file_list:
            file_names.append(file)
        return file_names
