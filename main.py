import base64
import logging
import os
import shutil
import sys
from pathlib import Path
from zipfile import ZipFile

import boto3
import pexpect
from botocore.vendored import requests
from dotenv import load_dotenv


def check_env_credentials(required_keys):

    missing_variables = required_keys.difference(os.environ.keys())

    if not missing_variables == set():
        logging.critical(' Missing environment variables:\n')
        for variable in missing_variables:
            print(variable)

        exit()


def set_git_ssh_password_from_env():

    try:
        pexpect.spawn('bash -c "ssh-agent -s"')

        child = pexpect.spawn('ssh-add')
        child.expect("Enter passphrase for /root/.ssh/id_rsa: ")
        child.sendline(os.getenv('GIT_KEY'))

    except Exception as error:
        print(error)


def clone_repository(origin: str):

    project_name = origin.split('/')[-1]
    path = 'tmp/' + project_name

    print('Cloning project {}\n'.format(project_name))

    command = 'git clone {} {}'.format(origin, path)
    os.system(command)


load_dotenv()
check_env_credentials({'GIT_KEY'})
set_git_ssh_password_from_env()
clone_repository('git@gitlab.com:auditoria-2.0/dashboard.git')
