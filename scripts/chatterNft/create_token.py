from brownie import ChatterNft, accounts, config
from scripts.helpful_scripts import get_mood, fund_chatter_token
import time

STATIC_SEED = 123

# def main():
#     dev = accounts.add(config['wallets']['from_key'])
#     chatter_Nft = ChatterNft[len(ChatterNft) - 1]
#     transaction = chatter_Nft.createToken("None", {'from': dev})
#     transaction.wait(1)
#     requestId = transaction.events['requestedToken']['requestId']
#     token_id = chatter_Nft.requestIdToTokenId(requestId)
#     time.sleep(90)
#     mood = get_mood(chatter_Nft.tokenIdToMood(token_id))
#     print('Chatter Mood of tokenId {} is {}'.format(token_id, mood))

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    chatter_nft = ChatterNft[len(ChatterNft) - 1]
    fund_chatter_token(chatter_nft.address)
    transaction = chatter_nft.createToken("None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    time.sleep(35)
    requestId = transaction.events["requestedToken"]["requestId"]
    token_id = chatter_nft.requestIdToTokenId(requestId)
    mood = get_mood(chatter_nft.tokenIdToMood(token_id))
    print("Chatter Mood of tokenId {} is {}".format(token_id, mood))