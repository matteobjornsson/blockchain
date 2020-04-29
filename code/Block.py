import json


class Block:

    def __init__(self, json_string):
        prevHash = 0
        timestamp = 0
        nonce = 0
        transactions = []

    def jsonToTx(self, _str):
        json_obj = json.loads(_str)
        return Transaction(json_obj['to_node'], json_obj['from_node'], json_obj['amount'], json_obj['timestamp'])

    def verify_transactions(self, start_state):
        #  start state from ledger is passed through from blockchain -> apply transactions
        #  I was thinking it would depend on where the method gets called
        # Yeah, not sure yet... But makes sense!
        pass

