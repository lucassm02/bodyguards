import logging
import os
import re
import shutil
from datetime import datetime

import boto3
import pytz
from botocore.exceptions import ClientError


def check_env_credentials(required_keys: list):

    missing_variables = required_keys.difference(os.environ.keys())

    if not missing_variables == set():
        logging.critical(' Missing environment variables:\n')
        for variable in missing_variables:
            print(variable)

        exit()


def validate_origin(origin: str):
    if not re.search(r'git@\w+\.[\w\.-]+:[\w\.-]+/[\.\w-]+.git', origin):
        logging.error(
            'incorrect git origin, use a origin that supports SSH.\nExample: git@github.com:lucassm02/bodyguards.git  ')
        exit()


def clone_repository(origin: str, path: str):

    validate_origin(origin)

    project_name = origin.split(':')[-1].replace('/', '-')
    project_path = '%s/%s' % (path, project_name)

    print('Cloning project %s\n' % project_name)

    command = 'git clone --bare %s %s' % (origin, project_path)
    os.system(command)

    return path


def get_dir_files(path: str):
    if os.path.isdir(path):
        return os.listdir(path)


def clear_folder(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)


def get_formatted_datetime():
    utc_now = pytz.utc.localize(datetime.utcnow())
    br_now = utc_now.astimezone(pytz.timezone("America/Sao_Paulo"))
    return br_now.strftime(r'%d-%m-%Y-%H-%M')


def generate_file_for_upload(project_path):
    try:

        file_name = '%s/backup-%s' % (project_path, get_formatted_datetime())

        shutil.make_archive(file_name, 'zip', project_path)

        return file_name + '.zip'

    except Exception as error:
        logging.exception(error)


def upload_file(file_name: str, bucket: str = None, object_name: str = None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # If S3 bucket was not specified, use BUCKET_NAME from .env
    if bucket is None:
        bucket = os.getenv('BUCKET_NAME')

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as error:
        logging.error(error)
        return False
    return True
