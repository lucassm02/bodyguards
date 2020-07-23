from dotenv import load_dotenv
from .helpers import check_env_credentials, clear_folder, clone_repository, generate_file_for_upload, upload_file


def main():

    __temp__ = 'temp'

    load_dotenv()
    check_env_credentials({
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_DEFAULT_REGION',
        'BUCKET_NAME'
    })
    clear_folder(__temp__)
    project_path = clone_repository(
        'git@gitlab.com:primi-ecommerce/frontend.git')
    file_path = generate_file_for_upload(project_path)
    file_name = file_path.replace(__temp__ + '/', '')
    response = upload_file(file_name=file_path, object_name=file_name)
    if response:
        clear_folder(__temp__)
