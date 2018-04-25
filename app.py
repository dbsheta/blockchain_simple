from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain
from transaction import Transaction

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    if len(blockchain.chain) == 0:
        proof = blockchain.proof_of_work(0)
        previous_hash = "0"
    else:
        last_block = blockchain.last_block
        previous_proof = last_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = Blockchain.hash(last_block)

    # Reward for mining
    transaction = Transaction(sender="0", receiver=node_identifier, amount=1)
    blockchain.add_new_transaction(transaction)

    block = blockchain.create_new_block(proof, previous_hash=previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'receiver', 'amount']
    if not all(k in values for k in required):
        return "Missing Values", 400

    transaction = Transaction(values['sender'], values['receiver'], values['amount'])
    index = blockchain.add_new_transaction(transaction)
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5000)
