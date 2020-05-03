from Block import Block
from Transaction import Transaction
from Ledger import Ledger
import datetime, hashlib, json


class BlockChain:
    """
    A class used to hold and manipulate a blockchain. Initialized with an associated ledger. BlockChain contents are
    stored to disk for node failure recovery.

    Attributes
    ----------
    ledger : Ledger
        asdf
    blockchain: List
        list of Block objects


    Methods
    -------
    process_block(block: Block)
        asdf

    """

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
        if block.verify_proof_of_work():
            print('proof of work check passed')
            if self.ledger.verify_and_add_transaction(block.transactions, block.index):
                print('verify tx check passed')
                self.add_block(block)
                return True
        return False

    def add_block(self, block):
        self.blockchain.insert(block.index, block)
        print('New block added to the block chain: \n', str(block))

    def get_last_block(self):
        return self.blockchain[-1]

    def __str__(self):
        blockchain_string = ''
        for block in self.blockchain:
            blockchain_string += '-'*75 + '\n'
            for k, v in block.__dict__.items():
                if k == 'transactions':
                    blockchain_string += k + ':\n'
                    for tx in v:
                        blockchain_string += '\t' + str(tx) + '\n'
                else:
                    blockchain_string += k + ': ' + str(v) + '\n'
            blockchain_string += '-' * 75 + '\n'
        return blockchain_string


if __name__ == '__main__':
    bc = BlockChain(Ledger())
    print("Initial blockchain: \n", bc)
    new_block = {
        'index': 1,
        'prevHash':'00000000000000000000000000000000000000000000000000000000000fffff',
        'timestamp' : str(datetime.datetime.now()),
        'nonce': 5,
        'transactions': [Transaction(_to='node1', _from='node2', amount=3.4),
                         Transaction(_to='node3', _from='node2', amount=2.1)]

    }
    new_block['transactions'] = [str(tx) for tx in new_block['transactions']]
    _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()
    new_block['hash'] = _hash
    new_block_json = json.dumps(new_block)
    b = Block(json_string = new_block_json)

    if bc.process_block(b):
        print("\n blockchain: \n", bc)
        print("ledger: \n", bc.ledger.blockchain_balances)



