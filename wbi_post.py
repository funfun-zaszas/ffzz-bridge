#!/usr/bin/env python3
import sys
import time
from web3.auto import w3
from contract import contract
from config import config

# Post a data request to the post_dr method of the WBI contract
def main():
    # set pre-funded account as sender
    account_addr = config["account"]["address"]

    # Check that the accout has enough balance
    balance = w3.eth.getBalance(account_addr)
    if balance == 0:
        raise Exception("Account does not have any funds")

    print(f"Got {balance} wei")

    with open(sys.argv[1], 'r') as my_file:
        dr_string = my_file.read()

    dr_id = contract.functions.post_dr(dr_string).transact(
        {"from": account_addr})
    post_tx_hash = bytes(dr_id).hex()
    print(
        f"Data request posted successfully! Ethereum transaction hash:\n0x{post_tx_hash}"
    )


if __name__ == '__main__':
    main()
