import json, hashlib, datetime
from Transaction import Transaction


class Block:

    def __init__(self, json_string: str = '', prevHash: str = '', timestamp: str = '', nonce: int = 0,
                 transactions: list = [], hash: str = '', index: int = 0):
        if json_string != '':
            json_obj = json.loads(json_string)
            self.prevHash = json_obj['prevHash']
            self.timestamp = json_obj['timestamp']
            self.nonce = int(json_obj['nonce'])
            self.transactions = [Transaction(x) for x in json_obj['transactions']]
            self.hash = json_obj['hash']
            self.index = int(json_obj['index'])
        else:
            self.prevHash = prevHash
            self.timestamp = timestamp
            self.nonce = nonce
            self.transactions = transactions
            self.index = index
            self.hash = hash

    def __str__(self):
        blockDict = self.__dict__
        blockDict['transactions'] = [str(tx) for tx in blockDict['transactions']]
        return json.dumps(blockDict)

    def verify_transactions(self, start_state):
        #  start state from ledger is passed through from blockchain -> apply transactions
        #  I was thinking it would depend on where the method gets called
        # Yeah, not sure yet... But makes sense!

        # we will have to implement our balance sheet first before writing this method, I think?
        pass

    def verify_proof_of_work(self):
        block_dict = self.__dict__
        block_dict['transactions'] = [str(tx) for tx in block_dict['transactions']]
        print("\nblock_dict in json format:\n", json.dumps(block_dict), '\n')
        incoming_hash = block_dict.pop('hash')
        print('print json block to verify, sans hash, followed by hash\n', json.dumps(block_dict), incoming_hash)
        verify_hash = hashlib.sha256(json.dumps(block_dict).encode()).hexdigest()
        print('verify_hash', verify_hash)
        print(type(verify_hash), type(incoming_hash))
        return verify_hash == incoming_hash


if __name__ == '__main__':
    new_block = {
        'prevHash':'e4d0ab7c39bbb38c2df7ee2689ae98f52a6099a5932b58c7339f8763dbaea2ec',
        'timestamp' : str(datetime.datetime.now()),
        'nonce': 5,
        'transactions': [Transaction(_to='node1', _from='node2', amount=12.5),
                         Transaction(_to='node3', _from='node2', amount=200.1)],
        'index': 4
    }
    new_block['transactions'] = [str(tx) for tx in new_block['transactions']]
    print('\n this is the exact string we are hashing for block b:\n', json.dumps(new_block),'\n')
    _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()
    new_block['hash'] = _hash

    new_block_json = json.dumps(new_block)
    b = Block(new_block_json)
    print('\njson representation of block b: \n', str(b), '\n')
    b2 = Block(str(b))
    print(b2.verify_proof_of_work())
