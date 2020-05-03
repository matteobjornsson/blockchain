from Ledger import *
from Transaction import Transaction
from Ledger import Ledger
from BlockChain import BlockChain
from Block import Block
from Messenger import Messenger
from threading import Thread
import datetime, json, hashlib, copy

class Node:
    difficulty = 1
    max = 'f'*64
    hash_difficulty = max.replace('f', '0', difficulty)

    def __init__(self, node_id: str):
        self.reset_mine_function = False
        self.stop_mine_function = False
        self.node_id = node_id
        self.ledger = Ledger()
        self.blockchain = BlockChain(self.ledger)
        self.messenger = Messenger(self.node_id, self)
        self.peers = [peer for peer in ['0', '1', '2', '3'] if peer != self.node_id]
        self.transaction_queue = []
        self.mine_thread = self.start_mining_thread()

    def start_mining_thread(self):
        t = Thread(
            target=self.create_mining_message_thread,
            daemon=True
        )
        t.start()
        return t

    def handle_incoming_message(self, msg):
        incoming_block = Block(msg['block'])
        if self.blockchain.process_block(incoming_block):
            delete_transactions = copy.deepcopy(incoming_block.transactions)
            self.transaction_queue = [x for x in self.transaction_queue if x not in delete_transactions]
            self.reset_mine_function = True

        # chain.process_block(block) #return true if block not discarded
        # if process_block returns true:
        #   delete all transactions in incoming block from transaction queue (node.update_tx_queue(block.tx))
        # reset mining process


    def update_tx_queue(self, transactions: list):
        # for each tx in transactions delete tx from self.transaction_queue
        pass

    def create_mining_message_thread(self):
        while True:
            new_block = self.mine_block()
            if new_block:
                self.send_block(new_block)
                print("mined a new block!: \n", new_block)
            else:
                self.reset_mine_function = False
                continue

    def mine_block(self) -> str:
        last_block = self.blockchain.get_last_block()
        transactions = copy.deepcopy(self.transaction_queue)
        new_block = {
            'index': last_block.index + 1,
            'prevHash': last_block.hash,
            'timestamp': str(datetime.datetime.now()),
            'nonce': 0,
            'transactions': transactions
        }
        new_block['transactions'] = [str(tx) for tx in new_block['transactions']]

        _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()

        while _hash > self.hash_difficulty:
            if not self.reset_mine_function:
                new_block['nonce'] += 1
                _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()
                print(_hash)
            else:
                _hash = ''
                break

        if _hash: # finished mine function uninterrupted, successfully mined new block
            new_block['hash'] = _hash
            new_block_json = json.dumps(new_block)
            # clear mined transactions from queue
            self.transaction_queue = [x for x in self.transaction_queue if x not in transactions]
            return new_block_json
        else: # mine function interrupted, returning empty string.
            return _hash

    def send_block(self, block: str):
        # send block to all known peers
        msg_dict = {'block': block}
        for peer in self.peers:
            self.messenger.send(msg_dict, peer)

if __name__ == '__main__':
    n = Node('0')
    # print(n.blockchain)
    # new_json_block = n.mine_block()
    # print(new_json_block)
    # new_block = Block(new_json_block)
    # print(new_block)
    # n.blockchain.process_block(new_block)
    # print(n.blockchain)