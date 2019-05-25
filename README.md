# ffzz-bridge
Bridge component to forward data requests between Ethereum contracts and Witnet

## Requirements

```sh
pip3 install msgpack toml web3
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
python3 wbi_post.py data_requests/air_quality.json
```

By default it will use the local ethereum testnet. This can be changed by
setting the ethereum client address as an environment variable:

```sh
export WEB3_PROVIDER_URI="http://127.0.0.1:8545"
```

