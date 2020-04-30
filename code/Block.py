import json
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
            self.hash = hash
            self.index = index

    def __str__(self):
        blockDict = self.__dict__
        blockDict['transactions'] = [str(tx) for tx in blockDict['transactions']]
        return json.dumps(blockDict)

    def verify_transactions(self, start_state):
        #  start state from ledger is passed through from blockchain -> apply transactions
        #  I was thinking it would depend on where the method gets called
        # Yeah, not sure yet... But makes sense!
        pass


if __name__ == '__main__':
    txs = [Transaction(_to='node1', _from='node2', amount=12.5), Transaction(_to='node3', _from='node2', amount=200.1)]
    b = Block(prevHash='222222222222222', timestamp='10:20pm', nonce='5',
              transactions=txs, hash='asdfasdfasdfasdf', index=5)
    print(str(b))
    b2 = Block(str(b))
    print(str(b2))
