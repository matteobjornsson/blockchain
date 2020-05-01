from Ledger import *
from Transaction import Transaction
from Ledger import Ledger
from BlockChain import BlockChain
from Block import Block
import datetime, json, hashlib, copy


class Node:
    difficulty = 1
    max = 'f'*64
    hash_difficulty = max.replace('f', '0', difficulty)

    def __init__(self):
        self.node_id = 0
        # messenger = ''#Messenger()
        self.ledger = Ledger()
        self.blockchain = BlockChain(self.ledger)
        self.peers = []
        self.transaction_queue = []

    def receive_block(self, block):
        # chain.process_block(block) #return true if block not discarded
        # if process_block returns true:
        #   delete all transactions in incoming block from transaction queue (node.update_tx_queue(block.tx))
        # reset mining process
        pass

    def update_tx_queue(self, transactions: list):
        # for each tx in transactions delete tx from self.transaction_queue
        pass

    def mine_block(self) -> str:
        last_block = self.blockchain.get_last_block()
        new_block = {
            'index': last_block.index + 1,
            'prevHash': last_block.hash,
            'timestamp': str(datetime.datetime.now()),
            'nonce': 0,
            'transactions': copy.deepcopy(self.transaction_queue)
        }
        new_block['transactions'] = [str(tx) for tx in new_block['transactions']]

        _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()

        while _hash > self.hash_difficulty:
            new_block['nonce'] += 1
            _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()
            print(_hash)

        new_block['hash'] = _hash
        new_block_json = json.dumps(new_block)
        return new_block_json

    def send_block(self, block: str):
        # send block to all known peers
        pass

if __name__ == '__main__':
    n = Node()
    print(n.blockchain)
    new_json_block = n.mine_block()
    print(new_json_block)
    new_block = Block(new_json_block)
    print(new_block)
    n.blockchain.process_block(new_block)
    print(n.blockchain)