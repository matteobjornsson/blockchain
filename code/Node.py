from code.Chain import *
from code.Ledger import *


class Node:

    def __init__(self):
        node_id = 0
        messenger = ''#Messenger()
        main_blockchain = BlockChain()
        ledger = Ledger()
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

