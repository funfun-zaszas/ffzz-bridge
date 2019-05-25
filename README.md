# ffzz-bridge
Bridge component to forward data requests between Ethereum contracts and Witnet

## Requirements

```sh
pip3 install toml web3
```

## Usage

* Run witnet node
* Update `config.toml`
* Run bridge:

```sh
# Event watcher, will block waiting for a PostDataRequest event
python3 wbi_watch.py

# Post a data request
# (can be skipped if the data request will be posted externally)
python3 wbi_post.py
```

