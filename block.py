import json
from time import time
from typing import List

from transaction import Transaction


class Block(object):
    def __init__(self, index: int, transactions: List[Transaction], proof: int, previous_hash: str):
        """
        Create an instance of Block
        :param index: block index
        :param transactions: list of transactions
        :param proof: proof
        :param previous_hash: hash of previous block
        """
        self._map = {
            'index': index,
            'timestamp': time(),
            'transactions': transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

    def __getitem__(self, item):
        return self._map[item]

    def __str__(self):
        return json.dumps(self._map, sort_keys=True)

    def __call__(self):
        return self._map
