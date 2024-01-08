import tomllib

import boto3

from .metadata_reader import lib_settings
from .utils import create_key_form_path, is_file_up_to_date


def update_files(ignore_raw_files=True) -> None:
    for file in lib_settings.data_dir.rglob("*.parquet"):
        if ignore_raw_files and ("raw" in file.name):
            continue
        if is_file_up_to_date(file):
            continue
        _upload_file_to_online_directory(file)


def _upload_file_to_online_directory(file_path):
    bucket = _get_bucket()
    key = create_key_form_path(file_path)
    with open(file_path, "rb") as file:
        bucket.put_object(ACL="public-read", Body=file, Key=key)


def _get_bucket(bucket_name="iran-open-data"):
    with open("tokens.toml", "rb") as file:
        token = tomllib.load(file)["arvan"]
    s3_resource = boto3.resource(
        "s3",
        endpoint_url="https://s3.ir-tbz-sh1.arvanstorage.ir",
        aws_access_key_id=token["access_key"],
        aws_secret_access_key=token["secret_key"],
    )
    bucket = s3_resource.Bucket(bucket_name)  # type: ignore
    return bucket
