from hashlib import sha256
from typing import Optional

from block import Block
from transaction import Transaction


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def add_new_transaction(self, transaction: Transaction) -> int:
        """
        Creates a new transaction to go into the next mined Block
        :param transaction: Instance of Transaction
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append(transaction())
        if self.last_block:
            index = self.last_block['index'] + 1
        else:
            index = 1
        return index

    def create_new_block(self, proof: int, previous_hash: Optional[str]) -> Block:
        """
        Create a new Block in the Blockchain and reset current transactions list
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
        block = Block(len(self.chain) + 1, self.current_transactions, proof, previous_hash)
        self.current_transactions = []
        self.chain.append(block())
        return block

    def proof_of_work(self, previous_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
         - Find a number 0' such that hash(00') contains leading 4 zeroes, where 0 is the previous 0'
         - 0 is the previous proof, and 0' is the new proof
        :param previous_proof: Previous proof
        :return: current proof
        """
        proof = 0
        while not self.is_valid_proof(previous_proof, proof):
            proof += 1
        return proof

    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None

    @staticmethod
    def hash(block: Block) -> str:
        """
        Generates SHA-256 hash for a block
        :param block: Block
        :return: hash of the block
        """
        block_string = str(block).encode()
        return sha256(block_string).hexdigest()

    @staticmethod
    def is_valid_proof(previous_proof: int, current_proof: int) -> bool:
        """
        Validates the Proof
        :param previous_proof:
        :param current_proof:
        :return:
        """
        guess = f'{previous_proof}{current_proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash.startswith('0000')
