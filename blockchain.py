#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 22:58:39 2020

@author: arbaazzakir
"""

#import libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urlib.parse import urlparse

#building general blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transaction}
        self.transaction = []
        self.chain.append(block)
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
     
    #proof of work
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    def add_transaction(self, sender, receiver, amount):
        self.transaction.append({'sender': sender,
                                 'receiver': receiver,
                                 'amount': amount})
            previous_block = self.get_previous_block()
            return previous_block['index'] + 1
    
#mining blockchain
        
#web app
app = Flask(__name__)

blockchain = Blockchain()

#mining a block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congrats, you just mined a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

#getting the full blockchain on ui
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'chain_length': len(blockchain.chain)}
    return jsonify(response), 200


#checks if blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain_validation = blockchain.is_chain_valid(blockchain.chain)
    if chain_validation is True:
        valid_state = 'Blockchain is valid'
    else:
        valid_state = 'Blockchain in not valid'
    response = {'message' : valid_state}
    
    return jsonify(response), 200
#run
app.run(host = '0.0.0.0', port = 5000)


    
    
    
    
    
    
 