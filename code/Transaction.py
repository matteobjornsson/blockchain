import hashlib, json, datetime


def jsonToTx(_str):
    json_obj = json.loads(_str)
    return Transaction(json_obj['to_node'], json_obj['from_node'], json_obj['amount'], json_obj['timestamp'])


class Transaction:

    def __init__(self, _to: str, _from: str, amount: float, timestamp: str = ''):
        self.to_node = _to #node id
        self.from_node = _from #own id
        self.amount = amount
        if timestamp:  # if there is an incoming timestamp (not empty string), i.e. building an existing tx, set it
            self.timestamp = timestamp
        else:  # otherwise generate new timestamp
            self.timestamp = str(datetime.datetime.now())
        self.unique_id = self.generateIDh()  # hash of to, from, amount, timestamp

    def toJSON(self):
        self_dict = {
            'to_node': self.to_node,
            'from_node': self.from_node,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        return json.dumps(self_dict)

    def generateIDh(self):
        hashMe = self.toJSON()
        return hashlib.sha256(hashMe.encode()).hexdigest()

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
