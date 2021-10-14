import requests
from pathlib import Path


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


breed_to_filepath = {
    "PUG": "./img/pug.png",
    "SHIBA_INU": "./img/shiba-inu.png",
    "ST_BERNARD": "./img/st-bernard.png",
}


def main():
    upload_to_ipfs(breed_to_filepath["PUG"])
    upload_to_ipfs(breed_to_filepath["SHIBA_INU"])
    upload_to_ipfs(breed_to_filepath["ST_BERNARD"])
