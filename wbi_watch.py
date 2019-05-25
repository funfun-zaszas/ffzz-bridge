#!/usr/bin/env python3
import json
import msgpack
import socket
import sys
import time
from web3.auto import w3
from contract import contract
from config import config


def witnet_send_dr(msg):
    sock = socket.create_connection((config["witnet_node"]["jsonrpc_ip"],
                                     config["witnet_node"]["jsonrpc_port"]))
    sock.sendall(msg.encode() + b"\n")


# Iterate over the lines of the socket
def socket_lines(sock):
    text = b""
    while True:
        data = sock.recv(1)
        text += data
        if data == b'\n':
            try:
                r = json.loads(text.decode())
                yield r
            except Exception as e:
                print(text.decode())
                print("JSON PARSE ERROR: " + str(e))
            text = b""


def wait_for_witnet_dr_result():
    # Subscribe to new blocks and wait until there is a block with a tally transaction
    sock = socket.create_connection((config["witnet_node"]["jsonrpc_ip"],
                                     config["witnet_node"]["jsonrpc_port"]))
    msg = '''{"jsonrpc":"2.0","method":"witnet_subscribe","params":["newBlocks"],"id":"1"}'''
    sock.sendall(msg.encode() + b"\n")

    socket_lines_iter = socket_lines(sock)
    # The first line is the response to the witnet_subscribe message,
    # with a subscription id that can be used to distinguish this subscription
    # from others, but we ignore it because there will only be one subscription
    _ = next(socket_lines_iter)
    for r in socket_lines_iter:
        try:
            print(r)
            tally = r["params"]["result"]["txns"]["tally_txns"][0]
            dr_hash = tally["dr_pointer"]
            tally_value_raw = tally["tally"]
            tally_value = msgpack.unpackb(bytes(tally_value_raw))
            print(f"Data request {dr_hash} has result {tally_value_raw}")
            return tally_value
        except Exception as e:
            print("No tally in block: " + str(e))
            pass


def handle_post_data_request(event):
    # We got a PostDataRequest event!
    dr_id = event.args.id
    print(f"Got data request with id {dr_id}")

    # Read the data request from the WBI contract
    dr_string = contract.functions.read_dr(dr_id).call()
    print(dr_string)

    # Send the data request to the witnet node
    witnet_send_dr(dr_string)

    # Wait for the data request result
    dr_result = wait_for_witnet_dr_result()

    print(f"Reporting data request with id {dr_id} with result {dr_result}")

    account_addr = config["account"]["address"]
    balance = w3.eth.getBalance(account_addr)
    if balance == 0:
        raise Exception("Account does not have any funds")

    print(f"Got {balance} wei")

    if dr_result in (True, False):
        contract.functions.report_result(dr_id, dr_result).transact(
            {"from": account_addr})
    else:
        try:
            dr_result = int(dr_result)
            # dr_result is an integer
            contract.functions.report_result_election(dr_id, dr_result).transact(
                {"from": account_addr})
        except:
            print(f"Unsupported result type: {dr_result}")


    print("Data request successfully relayed to Ethereum!")


def log_loop(event_filter, poll_interval):
    print("Waiting for PostDataRequest events...")
    while True:
        for event in event_filter.get_new_entries():
            handle_post_data_request(event)
            print("Waiting for PostDataRequest events...")
            ## Only handle first event
            #return
        time.sleep(poll_interval)


def main():
    current_block = w3.eth.blockNumber
    print(f"Current block: {current_block}")
    # Only listen to new events
    fromBlock = current_block
    ## Listen to all events
    #fromBlock = 0
    post_dr_filter = contract.events.PostDataRequest().createFilter(
        fromBlock=fromBlock)
    poll_interval = 2  # seconds
    log_loop(post_dr_filter, poll_interval)


if __name__ == '__main__':
    main()
