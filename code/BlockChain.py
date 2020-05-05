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
        a reference to the blockchain's associated ledger, created by Node.py
    blockchain: List
        list of Block objects constituting the blockchain


    Methods
    -------
    verify_block(block: Block)
        This method verifies the proof of work and transactions of a block and adds the block to the chain if valid.
    add_block(block: Block)
        Adds a block to the blockchain a its appropriate index
    get_last_block()
        Return last block in the chain.

    """

    def __init__(self, ledger):
        """
        Constructor initializes a BlockChain using a Genesis Block. Only used if no chain already on disk when Node.py
        starts up.

        :param ledger: Ledger. Reference to ledger passed to constructor for reference.
        """
        self.ledger = ledger
        self.blockchain = [  # Genesis block! as the first block in the chain the hashes are predetermined.
            Block(
                prevHash='0000000000000000000000000000000000000000000000000000000000000000',
                timestamp=str(datetime.datetime.now()),
                nonce=0,
                transactions=[],
                index=0,
                hash='000000000000000000000000000000000000000000000000000000000000000f'
            )
        ]
        #  TODO: pickledump and jsondump the chain to disk

    def verify_block(self, block) -> bool:
        """
        Method takes a block and verifies the PoW and transaction validity (which updates ledger if valid).
        If valid add block to chain.

        :param block: Block. Represents block object to be processed.
        :return: bool. Return True if valid block and added to ledger and chain, return False otherwise.
        """
        if block.index == self.get_last_block().index+1 and block.prevHash == self.get_last_block().hash:
            if block.verify_proof_of_work():
                print('proof of work check passed')
                # if transactions are valid verify_and_add will update the ledger and return true
                verified_bool, change = self.ledger.verify_transaction(block.transactions, block.index)
                if verified_bool:
                    self.ledger.add_balance_state(change[0], block.index)  # apply that state if none are negative
                    print('verify tx check passed')
                    #  add the block to the chain since PoW and tx are valid
                    self.add_block(block)
                    print("\nReceived Block added to Blockchain: \n", "Index: ", block.index, '\n', "Previous Hash: ",
                          block.prevHash, '\n', "Hash: ", block.hash, '\n')
                    return True
        return False
        #elif

    def add_block(self, block):
        """
        This method adds blocks to the chain and writes new chain to disk.

        :param block: Block. Block to be added to chain. Block is assumed to have been verified already
        :return: None
        """
        if block.index >= len(self.blockchain):
            self.blockchain.append(block)
        else:
            self.blockchain[block.index] = block
        #  TODO: write new chain to disk

    def get_last_block(self) -> Block:
        """
        Returns last block in the chain.

        :return: Block.
        """
        return self.blockchain[-1]

    def __str__(self) -> str:
        """
        Overrides native string representation of a BlockChain Object.

        :return: str. String representation of the BlockChain
        """
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

    if bc.verify_block(b):
        print("\n blockchain: \n", bc)
        print("ledger: \n", bc.ledger.blockchain_balances)



