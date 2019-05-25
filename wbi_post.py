#!/usr/bin/env python3
import sys
import time
from web3.auto import w3
from contract import contract
from config import config

dr_string = '''{"jsonrpc":"2.0","method":"buildDataRequest","id":1,"params":{"dro":{"pkh": "0000000000000000000000000000000000000000","data_request":{"not_before":0,"retrieve":[{"kind":"HTTP-GET","url":"https://api.coindesk.com/v1/bpi/currentprice.json","script":[152, 83, 204, 132, 146, 1, 163, 98, 112, 105, 204, 132, 146, 1, 163, 85, 83, 68, 204, 132, 146, 1, 170, 114, 97, 116, 101, 95, 102, 108, 111, 97, 116, 204, 130]}],"aggregate":{"script":[145,  146,  102,  32]},"consensus":{"script":[145,  146, 102,  32]},"deliver":[{"kind":"HTTP-GET","url":"https://hooks.zapier.com/hooks/catch/3860543/l2awcd/"},{"kind":"HTTP-GET","url":"https://hooks.zapier.com/hooks/catch/3860543/l1awcw/"}]},"value":1002,"witnesses":2,"backup_witnesses":1,"commit_fee":0,"reveal_fee":0,"tally_fee":0,"time_lock":0},"fee":0}}
'''


# Post a data request to the post_dr method of the WBI contract
def main():
    # set pre-funded account as sender
    account_addr = config["account"]["address"]

    # Check that the accout has enough balance
    balance = w3.eth.getBalance(account_addr)
    if balance == 0:
        raise Exception("Account does not have any funds")

    print(f"Got {balance} wei")

    dr_id = contract.functions.post_dr(dr_string).transact(
        {"from": account_addr})
    post_tx_hash = bytes(dr_id).hex()
    print(
        f"Data request posted successfully! Ethereum transaction hash:\n0x{post_tx_hash}"
    )


if __name__ == '__main__':
    main()
