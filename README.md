# FengWu-4DVar Demo

<!-- prettier-ignore -->
> [!NOTE]
> **Disclaimer**: This repository is a reproduction of the
> [FengWu-4DVar](https://github.com/OpenEarthLab/FengWu-4DVar) repository from
> OpenEarthLab for research and educational purposes. Please refer to the
> original repository for more details.

## Table of Contents

- [FengWu-4DVar Demo](#fengwu-4dvar-demo)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Environment Variables](#environment-variables)
  - [Download pre-trained model](#download-pre-trained-model)
  - [Setup for Google Colab environment (**recommended**)](#setup-for-google-colab-environment-recommended)
    - [Prerequisites](#prerequisites)
    - [Notebook](#notebook)
  - [Setup for local environment](#setup-for-local-environment)
    - [Prerequisites](#prerequisites-1)
    - [Download dataset](#download-dataset)
      - [Download dataset to Google Drive using Google Colab (**recommended**):](#download-dataset-to-google-drive-using-google-colab-recommended)
  - [Setup for local S3 storage](#setup-for-local-s3-storage)
    - [Setup data storage](#setup-data-storage)
      - [Setup Garage instance](#setup-garage-instance)
      - [Create buckets and keys](#create-buckets-and-keys)
      - [Uploading and downloading from Garage](#uploading-and-downloading-from-garage)
    - [Download dataset](#download-dataset-1)
      - [Download dataset to Google Drive using Google Colab (**recommended**):](#download-dataset-to-google-drive-using-google-colab-recommended-1)
      - [Download dataset directly to your S3 storage](#download-dataset-directly-to-your-s3-storage)
        - [Expose the Garage instance with Ngrok](#expose-the-garage-instance-with-ngrok)
        - [Download the dataset](#download-the-dataset)
  - [Getting Started](#getting-started)
  - [Notes](#notes)
  - [Acknowledgements](#acknowledgements)

## Description

This repo setup to run FengWu-4DVar on these environments:

- Google Colab.
- Local environment.
- Local S3 storage.

## Environment Variables

To run this project, you will need to add the following environment variables to
your `.env` file:

- Base configs:

  - `ONNX_MODEL_PATH`: Path to the ONNX model file. Default:
    `/content/drive/MyDrive/model.onnx`.

- Get data from Google Cloud (**recommended**):

  - `GCLOUD_BUCKET`: Google Cloud dataset from
    [ERA5 data from Google Cloud Public Dataset](https://cloud.google.com/storage/docs/public-datasets/era5).
    Default: `gs://gcp-public-data-arco-era5/ar/1959-2022-6h-1440x721.zarr`.

- Get data from s3:

  - `AWS_S3_ENDPOINT_URL`: S3 endpoint URL. Default: `localhost:3900`.
  - `AWS_ACCESS_KEY_ID`: S3 access key ID.
  - `AWS_SECRET_ACCESS_KEY`: S3 secret access key.

- Get data from local file:

  - `BASE_DATA_DIR`: Base data directory. Default:
    `/content/drive/MyDrive/data/content/data`.

E.g:

```
# .env
ONNX_MODEL_PATH="/content/drive/MyDrive/model.onnx"
GCLOUD_BUCKET="gs://gcp-public-data-arco-era5/ar/1959-2022-6h-1440x721.zarr"
AWS_S3_ENDPOINT_URL="localhost:3900"
AWS_ACCESS_KEY_ID="GK5f748179xxxx"
AWS_SECRET_ACCESS_KEY="d981f2ff47xxxx"
BASE_DATA_DIR="/content/drive/MyDrive/data/content/data"
```

You can also check out the file `.env.example` to see all required environment
variables.

## Download pre-trained model

- Download trained models from
  [OpenEarthLab/FengWu](https://github.com/OpenEarthLab/FengWu):

  - Fengwu without transfer learning (fengwu_v1.onnx):
    [Onedrive](https://pjlab-my.sharepoint.cn/:u:/g/personal/chenkang_pjlab_org_cn/EVA6V_Qkp6JHgXwAKxXIzDsBPIddo5RgDtGCBQ-sQbMmwg).

  - Fengwu with transfer learning (fengwu_v2.onnx, finetune the model with
    analysis data up to 2021):
    [Onedrive](https://pjlab-my.sharepoint.cn/:u:/g/personal/chenkang_pjlab_org_cn/EZkFM7nQcEtBve6MsqlWaeIB_lmpa__hX0I8QYOPzf-X6A).

## Setup for Google Colab environment (**recommended**)

### Prerequisites

This is tested within the following runtime:

- Runtime type: `Python 3`.
- Hardware accelerator: `CPU` + `High-RAM` (cost efficient but takes longer
  time).

Please

### Notebook

Please upload file [`notebooks/fengwu.ipynb`](./notebooks/fengwu.ipynb) to your
Google Colab environment.

You can adjust environment variables mentioned above beside the arguments passed
to file `cyclic_da.py` in the notebook.

## Setup for local environment

### Prerequisites

This repo is tested within the following environment:

- OS: `Ubuntu 22.04.5 LTS`.
- Python: `3.12`.
- Docker: `Docker version 27.5.1, build 9f9e405`.

### Download dataset

#### Download dataset to Google Drive using Google Colab (**recommended**):

1. Upload & run this script
   [data_prep_weather_forecast.ipynb](./notebooks/data_prep_weather_forecast.ipynb)
   on your Google Colab environment.

   This script will download a zip file that contains data from
   [ERA5 data from Google Cloud Public Dataset](https://cloud.google.com/storage/docs/public-datasets/era5)
   to your Google Drive.

   Then you have to download it to your local machine.

2. Extract the zip file:

   ```bash
   unzip era5.zip
   ```

## Setup for local S3 storage

### Setup data storage

If you already have a cloud S3 storage, you can skip this section.

#### Setup Garage instance

See more from the official guides:
[Quick Start](https://garagehq.deuxfleurs.fr/documentation/quick-start/) and
[Deployment on a cluster](https://garagehq.deuxfleurs.fr/documentation/cookbook/real-world/).

- We will setup a [Garage](https://garagehq.deuxfleurs.fr/) object storage to
  store the data. We will use docker compose to setup the storage:

  ```bash
  docker compose up -d
  ```

- The configuration file is in defined in `garage.toml`, you can follow this
  guide to setup the storage:

  ```bash
  cat > garage.toml <<EOF
  metadata_dir = "/tmp/meta"
  data_dir = "/tmp/data"
  db_engine = "sqlite"

  replication_factor = 1

  rpc_bind_addr = "[::]:3901"
  rpc_public_addr = "127.0.0.1:3901"
  rpc_secret = "$(openssl rand -hex 32)"

  [s3_api]
  s3_region = "garage"
  api_bind_addr = "[::]:3900"
  root_domain = ".s3.garage.localhost"

  [s3_web]
  bind_addr = "[::]:3902"
  root_domain = ".web.garage.localhost"
  index = "index.html"

  [k2v_api]
  api_bind_addr = "[::]:3904"

  [admin]
  api_bind_addr = "[::]:3903"
  admin_token = "$(openssl rand -base64 32)"
  metrics_token = "$(openssl rand -base64 32)"
  EOF
  ```

- You can use an alias for the docker command (optional):

  ```bash
  alias garage="docker exec -ti <container name> /garage"
  ```

- Check the status of the garage instance:

  ```bash
  garage status
  ```

  or using the following command:

  ```bash
  docker exec -ti <container name> /garage status
  ```

  You will se the node Id, save it for the next step.

- Assign region and capacity for the node:

  ```bash
  garage layout assign <NODE-ID> -z garage -c 20G
  ```

<!-- prettier-ignore -->
> [!NOTE]
> The `NODE-ID` you may type the first 4 characters of the node id.

<!-- prettier-ignore -->
> [!NOTE]
> You may increase the capacity if you have a large dataset.

- Review the layout before applying:

  ```bash
  garage layout show
  ```

  At the end of the output, you will see the version to apply.

- Apply the layout:

  ```bash
  garage layout apply --version <VERSION>
  ```

#### Create buckets and keys

- Create bucket:

  ```bash
  garage bucket create era-bucket
  ```

- Create an API key:

  ```bash
  garage key create era-app-key
  ```

  Then you will see the key and secret, save it for the next step:

  ```bash
  Key name: era-bucket-app-key
  Key ID: GK01efd7ca3614236dc903a81a # Save this key ID
  Secret key: 50a96dfd99be44d836457791f1321bdc96996f259ce04f7650d7e0c02ba1f9ee # Save this secret key for later use
  Can create buckets: false

  Key-specific bucket aliases:

  Authorized buckets:
  ```

- Allow the key to access the bucket:

  ```bash
  garage bucket allow \
    --read \
    --write \
    --owner \
    era-bucket \
    --key era-app-key
  ```

#### Uploading and downloading from Garage

- By default the package `awscli` is already installed from poetry. However, you
  can install it using the following command:

  ```bash
  pip install awscli
  ```

- Then create file `~/.awsrc`, you can use the `.awsrc.example` as a template:

  ```bash
  export AWS_ACCESS_KEY_ID=GK5f748179xxxx
  export AWS_SECRET_ACCESS_KEY=d981f2ff47xxxx
  export AWS_DEFAULT_REGION='garage'
  export AWS_ENDPOINT_URL='http://localhost:3900'
  ```

- Source the file:

  ```bash
  source ~/.awsrc
  ```

### Download dataset

#### Download dataset to Google Drive using Google Colab (**recommended**):

1. Upload & run this script
   [data_prep_weather_forecast.ipynb](./notebooks/data_prep_weather_forecast.ipynb)
   on your Google Colab environment.

   This script will download a zip file that contains data from
   [ERA5 data from Google Cloud Public Dataset](https://cloud.google.com/storage/docs/public-datasets/era5)
   to your Google Drive.

   Then you have to download it to your local machine.

2. Extract the zip file:

   ```bash
   unzip era5.zip
   ```

3. Copy dataset to S3 storage using AWS cli:

   ```bash
   aws s3 cp era5 s3://era-bucket/ --recursive
   ```

<!-- prettier-ignore -->
> [!NOTE]
> `era-bucket` is the name of the bucket that you have created.

#### Download dataset directly to your S3 storage

##### Expose the Garage instance with Ngrok

If you already have a cloud S3 storage, you can skip this section.

- Create an account on [Ngrok](https://ngrok.com/).

- Install [Ngrok](https://ngrok.com/):

  ```bash
  curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | sudo tee /etc/apt/sources.list.d/ngrok.list \
    && sudo apt update \
    && sudo apt install ngrok
  ```

  or you can try different installation methods from the official website.

- Configure Ngrok:

  ```bash
  ngrok config add-authtoken 2seHpxxxx
  ```

- Expose the garage instance:

  ```bash
  ngrok http http://localhost:3900
  ```

##### Download the dataset

1. Upload & run this script

   - Async:
     [async_data_prep_weather_forecast.ipynb](./notebooks/async_data_prep_weather_forecast.ipynb)
     on your Google Colab environment.

<!-- prettier-ignore -->
> [!NOTE]
> You can also copy function `uploadFileToS3` to sync
> [data_prep_weather_forecast.ipynb](./notebooks/data_prep_weather_forecast.ipynb)
> notebook.

2. This script will download data from
   [ERA5 data from Google Cloud Public Dataset](https://cloud.google.com/storage/docs/public-datasets/era5)
   to S3 storage that you have created.

## Getting Started

- Clone the repository:

  ```bash
  git clone https://github.com/DuckyMomo20012/FengWu-4DVar.git
  ```

- Change the directory:

  ```bash
  cd FengWu-4DVar
  ```

- Install the dependencies:

  ```bash
  poetry install
  ```

- Activate the virtual environment:

  ```bash
  poetry shell
  ```

- Run the script:

  ```bash
  python3 "cyclic_da.py" --start_time="2021-10-01 00:00:00" --end_time="2021-12-31 23:00:00"
  ```

## Notes

By default FengWu-4DVar is configured for (69, 128, 256) dataset shape, but the
model taken from the original FengWu has shape (168, 721, 1440), so we need to
do some preprocessing.

- Convert `/dataset/mask_random_*.npy` shape to (69, 721, 1440) in
  [/notebooks/mask_resize.ipynb](./notebooks/mask_resize.ipynb):

  ```python
  import numpy as np
  import cv2
  import glob

  # List of mask files to resize

  mask_files = ["./dataset/mask_random_005.npy", "./dataset/mask_random_010.npy",
  "./dataset/mask_random_015.npy"]

  # Target size

  target_shape = (69, 721, 1440) # (depth, height, width)

  for file in mask_files: # Load mask mask = np.load(file) # Shape: (69, 128, 256)
  print(f"Resizing {file}: Original shape {mask.shape}")

      # Prepare resized array
      mask_resized = np.zeros(target_shape, dtype=np.uint8)

      # Resize each slice independently
      for i in range(69):
          mask_resized[i] = cv2.resize(mask[i], (1440, 721), interpolation=cv2.INTER_NEAREST)

      # Save resized mask
      output_file = file.replace(".npy", "_resized.npy")
      np.save(output_file, mask_resized)

      print(f"Saved {output_file}: New shape {mask_resized.shape}")
  ```

## Acknowledgements

- [Towards a Self-contained Data-driven Global Weather Forecasting Framework](https://proceedings.mlr.press/v235/xiao24a.html).
- [OpenEarthLab/FengWu repository](https://github.com/OpenEarthLab/FengWu).
- [OpenEarthLab/FengWu-4DVar repository](https://github.com/OpenEarthLab/FengWu-4DVar).
- [Garage](https://garagehq.deuxfleurs.fr/): An open-source distributed object
  storage service tailored for self-hosting.
- [ERA5 data from Google Cloud Public Dataset](https://cloud.google.com/storage/docs/public-datasets/era5):
  Analysis-Ready, Cloud Optimized (ARCO) ERA5 data.
