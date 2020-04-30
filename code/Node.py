from Chain import *
from Ledger import *
from Transaction import Transaction
from Ledger import Ledger
from BlockChain import BlockChain
import datetime, json, hashlib


class Node:
    difficulty = 3
    max = 'f'*64
    hash_difficulty = max.replace('f', '0', difficulty)

    def __init__(self):
        node_id = 0
        # messenger = ''#Messenger()
        self.ledger = Ledger()
        self.blockchain = BlockChain(self.ledger)
        peers = []
        transaction_queue = []

    def receive_block(self, block):
        # chain.process_block(block) #return true if block not discarded
        # if process_block returns true:
        #   delete all transactions in incoming block from transaction queue (node.update_tx_queue(block.tx))
        # reset mining process
        pass

    def update_tx_queue(self, transactions: list):
        # for each tx in transactions delete tx from self.transaction_queue
        pass

    def mine_block(self):
        # get prevHash and index
        # get transactions
        nonce = 0
        new_block = {
            'prevHash': 'e4d0ab7c39bbb38c2df7ee2689ae98f52a6099a5932b58c7339f8763dbaea2ec',
            'timestamp': str(datetime.datetime.now()),
            'nonce': nonce,
            'transactions': [Transaction(_to='node1', _from='node2', amount=12.5),
                             Transaction(_to='node3', _from='node2', amount=200.1)],
            'index': 4
        }
        new_block['transactions'] = [str(tx) for tx in new_block['transactions']]

        _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()

        while _hash > self.hash_difficulty:
            new_block['nonce'] += 1
            _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()
            print(_hash)

        new_block['hash'] = _hash
        new_block_json = json.dumps(new_block)
        print(new_block_json)

        # grab prev hash to include in block
        # collect new transactions to mine
        # timestamp
        # nonce = 0
        # while hash is less than correct difficulty:
        #    increment nonce
        # when hash is correct difficulty add to own chain & send it
        #   remove mined transactions from queue node.update_tx_queue(transactions)
        # if a block is received mid mine, abort mining, start again on new block
        pass

    def send_block(self, block: str):
        # send block to all known peers
        pass

if __name__ == '__main__':
    n = Node()
    n.mine_block()