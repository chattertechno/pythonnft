import os
from brownie import ChatterNft, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_mood
from pathlib import Path
import requests
import json

def main():
    print("Working on " + network.show_active())
    chatter_nft = ChatterNft[len(ChatterNft) - 1]
    number_of_chatter_nfts = chatter_nft.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_chatter_nfts)
    )
    write_metadata(number_of_chatter_nfts, chatter_nft)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        token_metadata = sample_metadata.metadata_template
        mood = get_mood(nft_contract.tokenIdToMood(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)
            + "-"
            + mood
            + ".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(
                    metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            token_metadata["name"] = get_mood(
                nft_contract.tokenIdToMood(token_id)
            )
            token_metadata["description"] = "An adorable {} guy!".format(
                token_metadata["name"]
            )
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    mood.lower().replace('_', '-'))
                image_to_upload = upload_to_ipfs(image_path)
            # image_to_upload = (
            #     mood_to_image_uri[mood] if not image_to_upload else image_to_upload
            # )
            token_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(token_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri