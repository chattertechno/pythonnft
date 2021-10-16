from brownie import ChatterNft, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import get_mood, OPENSEA_FORMAT

dog_metadata_dic = {
    "SAD": "https://ipfs.io/ipfs/QmQB3Dm1SfdiWbhxAxuWr6FsQhLBnJo1wmtnCpuUFT2UGJ?filename=0-SAD.json",
    "ANGRY": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "HAPPY": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

def main():
    print("Working on " + network.show_active())
    chatter_nft = ChatterNft[len(ChatterNft) - 1]
    number_of_chatter_nfts = chatter_nft.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_chatter_nfts)
    )
    for token_id in range(number_of_chatter_nfts):
        mood = get_mood(chatter_nft.tokenIdToMood(token_id))
        if not chatter_nft.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, chatter_nft,
                         dog_metadata_dic[mood])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))
            print(
                "Your tokenURI is: {}".format(
                    chatter_nft.tokenURI(token_id)
                )
            )


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')