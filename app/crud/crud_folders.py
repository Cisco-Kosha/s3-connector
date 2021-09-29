from typing import List, Any

import json
import boto3
import os


from app.core.config import settings

s3 = settings.s3_init()
bucket_name = settings.get_bucket_name()


class CRUDFolders:
   pass