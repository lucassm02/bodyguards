import logging
import os
import shutil
from dotenv import load_dotenv


def check_env_credentials(required_keys):

    missing_variables = required_keys.difference(os.environ.keys())

    if not missing_variables == set():
        logging.critical(' Missing environment variables:\n')
        for variable in missing_variables:
            print(variable)

        exit()


def clone_repository(origin: str):

    project_name = origin.split('/')[-1]
    path = 'tmp/' + project_name

    print('Cloning project {}\n'.format(project_name))

    command = 'git clone --bare {} {}'.format(origin, path)
    os.system(command)


def get_dir_files(path):
    if os.path.isdir(path):
        return os.listdir(path)


def clear_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)


def check_for_upload(path, callback=None):

    if len(get_dir_files(path)) > 1:
        clear_folder(path)
        if not callback is None:
            callback()


def run():

    temporary_folder_path = './tmp'

    load_dotenv()
    check_env_credentials({'AWS_KEY', 'AWS_SECRET', 'BUCKET_NAME'})
    clear_folder(temporary_folder_path)
    clone_repository('git@gitlab.com:auditoria-2.0/dashboard.git')
    check_for_upload(temporary_folder_path, run)


if __name__ == '__main__':
    run()
