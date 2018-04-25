import json


class Transaction(object):
    def __init__(self, sender: str, receiver: str, amount: int):
        """
        Create an instance of Transaction
        :param sender: Sender id
        :param receiver: Receiver id
        :param amount: Amount to be transacted
        """
        self._map = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }

    def __getitem__(self, item):
        return self._map[item]

    def __repr__(self):
        return json.dumps(self._map, sort_keys=True)

    def __call__(self):
        return self._map
