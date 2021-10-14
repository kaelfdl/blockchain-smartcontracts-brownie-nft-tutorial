import json
import os
import requests
from pathlib import Path
from brownie import AdvancedCollectible, network
from scripts.advanced_collectible.set_token_uri import set_token_uri
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from scripts.advanced_collectible.upload_to_ipfs import upload_to_ipfs

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_filename}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed}"
            print(collectible_metadata)
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_uri
            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                token_uri = upload_to_ipfs(metadata_filename)
            if os.getenv("SET_URI") == "true":
                set_token_uri(token_id, advanced_collectible, token_uri)
