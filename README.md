# Casper Python SDK

Python library for interacting with a CSPR node.


What is casper-client-py ?
------------------------------------------------------

The python client is published as pycspr: **PY**thon **C**a**SP**e**R**.  It's goal is to streamline client side experience of interacting with a casper node.


How To: Install ?
------------------------------------------------------

```
pip install pycspr
```

How To: Query a node ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_query_nodes.py).

How To: Transfer funds between 2 accounts ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_transfer.py).

How To: Delegate funds to a validator ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_delegate.py).

How To: Undelegate funds from a validator ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_undelegate.py).

How To: Stake funds as a validator ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_stake.py).

How To: Unstake funds as a validator ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_unstake.py).

How To: Install a smart contract ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_install_a_contract.py).

How To: Invoke a smart contract ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_invoke_a_contract.py).

How To: Query a smart contract ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_query_contracts.py).

How To: Speculatively execute a deploy ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_speculatively_execute_a_deploy.py).

How To: Hash data ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_hash_data.py).

How To: Create Key Pairs ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_create_key_pairs.py).

How To: Apply a checksum ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_apply_a_checksum.py).

How To: Await Events  ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_await_events.py).

How To: Consume Events  ?
------------------------------------------------------

See [here](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_consume_events.py).

How To: Run unit tests against a CCTL network ?
------------------------------------------------------

Ensure you are running a [CCTL](https://github.com/casper-network/cctl) network and have exported the CCTL environment variable.

```
cd YOUR_WORKING_DIRECTORY
pipenv shell
pytest ./tests
````
