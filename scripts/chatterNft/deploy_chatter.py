from brownie import ChatterNft, accounts, network, config
from scripts.helpful_scripts import fund_chatter_token

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(network.show_active())
    publish_source = True
    chatterNft = ChatterNft.deploy(
        config['networks'][network.show_active()]['vrf_coordinator'],
        config['networks'][network.show_active()]['link_token'],
        config['networks'][network.show_active()]['key_hash'],
        {"from": dev},
        publish_source=publish_source
    )
    fund_chatter_token(chatterNft)
    return chatterNft