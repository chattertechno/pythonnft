from brownie import ChatterNft
from scripts.helpful_scripts import fund_chatter_token

def main():
    chatter_Nft = ChatterNft[len(ChatterNft) - 1]
    fund_chatter_token(chatter_Nft)