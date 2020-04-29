import hashlib, json, datetime

class NewTransaction:
    def newTx(_to: str, _from: str, amount: float) -> str:
        unique_id = self.generateIDh()  # hash of to, from, amount, timestamp

    def generateIDh():
        hashMe = self.toJSON()
        return hashlib.sha256(hashMe.encode()).hexdigest()

class Transaction:

    def __init__(self, json_string):
        json_obj = json.loads(json_string)
        self.to_node = json_obj['to_node'] #node id
        self.from_node =json_obj['from_node'] #own id
        self.amount = json_obj['amount']
        self.timestamp = json_obj['timestamp']
        self.uniqueID = json_obj


    def toJSON(self):
        self_dict = {
            'to_node': self.to_node,
            'from_node': self.from_node,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        return json.dumps(self_dict)

    def __str__(self):
        return json.dumps(self.__dict__)

    def __equals__(self, _in):
        return _in.unique_id == self.unique_id


if __name__ == '__main__':
    t = Transaction('node1', 'node2', 12.5)
    t.unique_id = t.generateIDh()
    print(str(t))
    jsonT = str(t)
    backToT = jsonToTx(jsonT)
    print(type(backToT))
    print(str(backToT))
