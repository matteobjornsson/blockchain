from Transaction import Transaction


class Ledger:

    def __init__(self):
        self.blockchain_balances = [{'node0': 10, 'node1': 10, 'node2': 10, 'node3': 10}]

    def verify_and_add_transaction(self, transactions, index) -> bool:
        change = self.blockchain_balances[index-1]
        for tx in transactions:
            change[tx.from_node] -= tx.amount
            change[tx.to_node] += tx.amount
        for v in change.values():
            if v < 0:
                return False
        self.add_transaction(change, index)
        return True

    def add_transaction(self, balance, index):
        self.blockchain_balances.insert(index, balance)

    def get_curr_balance_for_node(self, node):
        return self.blockchain_balances[-1][node]

    def get_total_currency_in_chain(self):
        _sum = 0
        for v in self.blockchain_balances[-1].values():
            _sum += v
        return _sum


if __name__ == '__main__':
    transactions = [Transaction(_to='node1', _from='node2', amount=1.5),
                    Transaction(_to='node3', _from='node2', amount=3.6)]
    nodes = ['node0', 'node1', 'node2', 'node3']
    L = Ledger()
    L.verify_and_add_transaction(transactions, 1)
    for node in nodes:
        print('Balance: ', node, ': ', L.get_curr_balance_for_node(node))
    print("total currency: ", L.get_total_currency_in_chain())