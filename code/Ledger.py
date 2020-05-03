from Transaction import Transaction


class Ledger:
    """
    This class is designed to hold a list of balance states of the blockchain network where each state corresponds to
    the state of the network after the transactions within its associated block were applied to the network balances.
    BlockChain[1] -> Ledger[1]

    Attributes
    ----------
    blockchain_balances : list.
        This list holds all balance states of the blockchain, each state corresponds to a new block added to the chain.

    Methods
    ----------
    verify_and_add_transaction(transactions: list of Transaction objects, index: int)
        Takes transaction objects and applies them to the ledger at index. If any balance is negative return false.
    add_balance_state(balance: dict, index: int)
        Adds a ledger state (in form of dictionary of peers and balances) to the ledger list at index.
    get_curr_balance_for_node(node: str)
        Returns current balance of a given node (as defined in last entry in ledger)
    get_total_currency_in_chain()
        Returns sum of all member balances (represents coin in circulation)
    """

    def __init__(self):
        """
        Constructor for the Ledger. Initializes balance of genesis block to introduce init currency into blockchain.
        """
        self.blockchain_balances = [{'node0': 10, 'node1': 10, 'node2': 10, 'node3': 10}]  # initial bc balance

    def verify_and_add_transaction(self, transactions, index) -> bool:
        """
        Takes transaction objects and applies them to the ledger at index. If any balance is negative return false.

        :param transactions: list. List of Transaction objects to verify
        :param index: int. index at which the transactions are applied (equal to block index)
        :return: bool. Return false if transactions cause any balance to go negative.
        """

        change = self.blockchain_balances[index-1]  # get previous state
        for tx in transactions:  # apply all transactions to that state
            change[tx.from_node] -= tx.amount
            change[tx.to_node] += tx.amount
        for v in change.values():
            if v < 0:
                return False
        self.add_balance_state(change, index)  # apply that state if none are negative
        return True

    def add_balance_state(self, balance, index):
        """
        Adds a ledger state (in form of dictionary of peers and balances) to the ledger list at index.

        :param balance: dict. Dictionary of peer keys and balance values.
        :param index: int.
        :return: None
        """
        self.blockchain_balances.insert(index, balance)

    def get_curr_balance_for_node(self, node) -> float:
        """
        Returns current balance of a given node (as defined in last entry in ledger)

        :param node: str. Name of node in question
        :return: float.
        """
        return self.blockchain_balances[-1][node]

    def get_total_currency_in_chain(self) -> float:
        """
        Returns sum of all member balances (represents coin in circulation)
        :return: float.
        """
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