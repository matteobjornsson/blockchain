from Block import Block
from Transaction import Transaction
import datetime, hashlib, json


class BlockChain:

    def __init__(self, ledger):
        self.ledger = ledger
        self.blockchain = [Block(
            prevHash='0000000000000000000000000000000000000000000000000000000000000000',
            timestamp= str(datetime.datetime.now()),
            nonce= 0,
            transactions= [],
            index= 0,
            hash='00000000000000000000000000000000000000000000000000000000000fffff'
        )]
        #pickledump and jsondump the chain to disk

    def process_block(self, block) -> bool:
        verified_pow =
        if block.verify_proof_of_work():
            if self.ledger.verify_and_add_transaction():
                self.add_block(block)
                return True
        return False

    def add_block(self, block):
        self.blockchain.insert(block.index, block)
        pass

    def get_last_block(self):
        return self.blockchain[-1]

