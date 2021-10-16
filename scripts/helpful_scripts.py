from brownie import ChatterNft, accounts, config, interface, network


OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"
def get_mood(mood_number):
    switch = {1:'SAD' , 2: 'ANGRY', 3: 'HAPPY'}
    return switch[mood_number]

def fund_chatter_token(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])
    link_token = interface.LinkTokenInterface(config['networks'][network.show_active()]['link_token'])
    link_token.transfer(nft_contract, 100000000000000000, {'from': dev})
