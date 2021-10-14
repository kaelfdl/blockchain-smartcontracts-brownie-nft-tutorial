import json
from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account

breed_to_uri = {
    "PUG": "https://ipfs.io/ipfs/Qmd4T7PnUNnyKbTChx9Ui6kwpffeifvd2RGeMCQZQQfey2?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmV4rxqNmRUZtv62zixYfRDgRT7KiJ38h34LCWnzfiqzxT?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/Qmbsq7jxXnHdcnKHcDm9UXh7yEMbbkovnhkTEF9LFie6sr?filename=0-ST_BERNARD.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_token_uri(token_id, advanced_collectible, breed_to_uri[breed])


def set_token_uri(token_id, nft_contract, token_uri):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can now view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 mins and hit the refresh metadata button.")
