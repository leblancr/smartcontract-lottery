from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config['networks'][network.show_active()]['eth_usd_price_feed'],
        {'from': account}
    )

    # Ether = Wei / 10**18
    # Wei = Ether * 10**18
    # Dollars = Ether * Exchange rate
    current_eth_price_in_wei = lottery.getCurrentEthPriceInWei()
    current_eth_price_in_eth = current_eth_price_in_wei / 10**18
    entrance_fee_in_usd = lottery.getEntranceFeeInUsd()
    entrance_fee_in_wei = lottery.getEntranceFeeInWei()
    fee_in_eth = entrance_fee_in_usd / current_eth_price_in_wei  # 0.0000137117942995
    fee_in_usd = current_eth_price_in_wei * fee_in_eth
    conversion_factor = 1 / (current_eth_price_in_wei / 10**18)  # wie times this to usd

    print("Ether = Wei / 10**18")
    print("Wei = Ether * 10**18")
    print(f'entrance_fee_in_wei = {entrance_fee_in_wei}')
    print(f"1. Convert Wei to Ether = Wei / 10**18 = {entrance_fee_in_wei} / 10**18 = {entrance_fee_in_wei / 10**18} ")
    entrance_fee_in_ether = entrance_fee_in_wei / 10**18  # shift left 18
    print(f'entrance_fee_in_ether = {entrance_fee_in_ether}')
    print("2. Convert Ether to dollars = Ether * Exchange rate")
    print(f'entrance_fee_in_usd = {entrance_fee_in_ether} * {current_eth_price_in_eth} = {entrance_fee_in_ether * current_eth_price_in_eth}')
    
    assert Web3.toWei(fee_in_eth, 'ether') >= 50  # 
    