import hashlib, json, datetime


class Transaction:
    def __init__(self, json_string = '', _to: str = '', _from: str = '', amount: float = 0.0):
        if json_string != '':
            json_obj = json.loads(json_string)
            self.to_node = json_obj['to_node']
            self.from_node = json_obj['from_node']
            self.amount = json_obj['amount']
            self.timestamp = json_obj['timestamp']
            self.unique_id = json_obj['unique_id']
        else:
            self.to_node = _to #node id
            self.from_node = _from #own id
            self.amount = amount
            self.timestamp = str(datetime.datetime.now())
            self.unique_id = self.generateIDh()  # hash of to, from, amount, timestamp

    def txHeaderToJSON(self):
        self_dict = {
            'to_node': self.to_node,
            'from_node': self.from_node,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        return json.dumps(self_dict)

    def generateIDh(self):
        hashMe = self.txHeaderToJSON()
        return hashlib.sha256(hashMe.encode()).hexdigest()

    def __str__(self):
        return json.dumps(self.__dict__)

    def __equals__(self, _in):
        return _in.unique_id == self.unique_id



if __name__ == '__main__':
    t = Transaction(_to='node1', _from='node2', amount=12.5)
    print(str(t))
    jsonT = str(t)
    backToT = Transaction(json_string=jsonT)
    print(type(backToT))
    print(str(backToT))
