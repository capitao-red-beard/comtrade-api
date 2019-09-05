import os
from pathlib import Path

import pandas as pd
from azure.storage.blob import BlockBlobService
from fastparquet import ParquetException
from fastparquet import ParquetFile
from fastparquet import write

import keyring

account_name = "samsmdpblobdev02"
container_name = "raw"
block_blob_service = BlockBlobService(
    account_name=account_name,
    account_key=keyring.get_password("azure_blob", account_name),
)
local_path = Path(os.path.expanduser("~/Documents"))


def create_blob_from_path(blob_name, file_name):
    block_blob_service.create_blob_from_path(container_name, blob_name, file_name)


def update_blob_from_path(blob_name, data_frame):
    block_blob_service.get_blob_to_path(container_name, blob_name, local_path)

    try:
        pf_local = ParquetFile(local_path)
        df_local = pf_local.to_pandas()

    except ParquetException:
        print(
            "Failed to convert blob to parquet or create pandas from parquet "
            + str(ParquetException)
        )

    df_to_submit = pd.concat([df_local, data_frame])

    try:
        write(local_path, df_to_submit)

    except ParquetException:
        print("Failed to convert pandas to parquet " + str(ParquetException))

    block_blob_service.create_blob_from_path(container_name, blob_name, local_path)


def delete_blob(blob_name):
    block_blob_service.delete_blob(container_name, blob_name)


def get_blob_list():
    blobs = []
    generator = block_blob_service.list_blobs(container_name)

    for blob in generator:
        blobs.append("Blob Name: {}".format(blob.name))

    return blobs


def get_blob_url(blob_name):
    return block_blob_service.make_blob_url(container_name, blob_name)


def create_container():
    block_blob_service.create_container(container_name)


def delete_container():
    block_blob_service.delete_container(container_name)


def get_container_list():
    containers = []
    generator = block_blob_service.list_containers()

    for container in generator:
        containers.append("Container Name: {}".format(container.name))

    return containers


def generate_blob_name(csv_file):
    return Path()


def to_parquet(csv_file):
    df = pd.read_csv(csv_file)

    return df.to_parquet("output.parquet")
