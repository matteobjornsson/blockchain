from Ledger import *
from Transaction import Transaction
from Ledger import Ledger
from BlockChain import BlockChain
from Block import Block
from Messenger import Messenger
from threading import Thread
from time import sleep
import datetime, json, hashlib, copy


class Node:
    """
    A class used to represent a Miner node in a BlockChain network. Initialized with node ID string. This class
    sets up a thread that continually mines new blocks from a transaction queue, meeting a predefined hash
    difficulty. Node uses Messenger (SQS) to send and receive messages from other nodes.

    Attributes
    ----------
    difficulty : int
        indicates hash difficulty for mining blocks, integer represents number of leading 0s required
    max : str
        reference for maximum possible hash value
    hash_difficulty : str
        reference for hash difficulty as represented by a 64 char hexadecimal hash
    node_id : str
        name of node (in this case '0', '1', '2', or '3'
    ledger : Ledger
        ledger associated with the blockchain for checking validity of transactions and peer balances
    blockchain : BlockChain
        this is the node's copy of the blockchain for reference and updating
    messenger : Messenger
        a messaging layer used by the node to send and receive blocks and transactions from other miners
    peers : list
        a list of peer nodes, members of the BlockChain network
    transaction_queue : list
        a list of incoming transactions to be mined into a block
    reset_mine_function : bool
        flag for when a new block is discovered, when true node resets flag and begins mining on new block instead
    stop_mine_function : bool
        flag for stopping the mining thread
    mine_thread : thread
        a stored reference to the mining thread for accessing the thread if necessary

    Methods
    -------
    start_mining_thread()
        Starts the thread that continually mines new blocks to add to the chain.
    handle_incoming_message()
        interface required for the Messenger class, handles incoming messages from the Messenger class.
    mining_message_thread()
        continually mines new blocks on current blockchain, resets function when new block received
    mine_block()
        the actual function that generates a hash for a new block to add to the blockchain
    send_block(block: str)
        sends newly mined blocks to all peers

    """
    difficulty = 3
    max = 'f'*64
    hash_difficulty = max.replace('f', '0', difficulty)
    print('hash difficulty: ', hash_difficulty)

    def __init__(self, node_id: str):
        """
        Constructor for the Node class.

        :param str node_id: one of '0', '1', '2', or '3', the possible nodes in network
        """
        self.node_id = node_id
        #  TODO: check disk for existing ledger and blockchain. Only make new instance if not found.
        self.ledger = Ledger()
        self.blockchain = BlockChain(self.ledger)

        self.messenger = Messenger(self.node_id, self)
        self.peers = [peer for peer in ['0', '1', '2', '3'] if peer != self.node_id]
        self.transaction_queue = []
        self.reset_mine_function = False
        self.stop_mine_function = False
        self.mine_thread = self.start_mining_thread()

    def start_mining_thread(self) -> Thread:
        """
        Starts the thread that continually mines new blocks to add to the chain.

        :return: mining thread
        """
        t = Thread(
            target=self.mining_message_thread
        )
        t.start()
        return t

    def handle_incoming_message(self, msg: dict):
        """
        Handles incoming messages from the Messenger class in dictionary format.

        :param msg: dict. Message attributes represented as string key value pairs.
        :return: None
        """
        if msg['type'] == 'Transaction':  # if transaction append to tx queue
            self.transaction_queue.append(Transaction(msg['contents']))

        elif msg['type'] == 'Block':  # if block process and reset mine function if valid
            print("Incoming Block Received! \n")  # debugging print statement
            # Nodes must always mine on the longest chain, so any mining in progress needs to be reset
            self.reset_mine_function = True
            incoming_block = Block(msg['contents'])
            # process block returns true if it is valid and added to blockchain and ledger
            if self.blockchain.process_block(incoming_block):
                # if the block is valid, then we need to remove all transactions from our own tx queue
                delete_transactions = copy.deepcopy(incoming_block.transactions)
                self.transaction_queue = [x for x in self.transaction_queue if x not in delete_transactions]
                print('transactions after deletion ', self.transaction_queue)


    def mining_message_thread(self):
        """
        Function to be threaded. Continually mines new blocks on current blockchain, watches for new blocks to mine on

        :return: None
        """
        while not self.stop_mine_function:  # always run unless stop flag is true
            # Json string is what we will send to other nodes.
            if True: # self.transaction_queue:  # check if tx queue is empty
                # mine_block() returns empty ('false') string if mining was interrupted by discovery of new block
                new_block_json = self.mine_block()
                if new_block_json:  # i.e if we mined a block uninterrupted
                    new_block = Block(new_block_json)  # Block object is what we will add to own blockchain
                    #  if valid, verified_bool returns True, with new balance
                    #  if not valid, verified_bool returns False with list of bad transaction IDs
                    verified_bool, return_value = self.ledger.verify_transaction(new_block.transactions, new_block.index)
                    print('verified transaction , returned ', str(verified_bool))
                    if verified_bool:
                        print('verification successful change of ', return_value)
                        self.ledger.add_balance_state(return_value[0], new_block.index)
                        self.blockchain.add_block(new_block)
                        self.send_msg(new_block_json, 'Block')
                        print("mined a new block!: \n", new_block)
                else:  # this will only occur if mining had been interrupted, so we need to reset flag and start again
                    print('verification unsuccessful, returned following transactions ', return_value)
                    self.transaction_queue = [tx for tx in self.transaction_queue if tx.unique_id not in return_value]
                    self.reset_mine_function = False
                    continue
            else:
                sleep(.5)

    def mine_block(self) -> str:
        """
        the actual function that generates a hash for a new block to add to the blockchain

        :return: str. Returns empty string if interrupted, otherwise JSON string representation of a newly mined block
        """
        last_block = self.blockchain.get_last_block()
        transactions = copy.deepcopy(self.transaction_queue)
        #  make a new block with everything but the hash
        new_block = {
            'index': last_block.index + 1,
            'prevHash': last_block.hash,
            'timestamp': str(datetime.datetime.now()),
            'nonce': 0,
            'transactions': transactions
        }
        # change the transaction objects into strings so it can be dumped into JSON format
        new_block['transactions'] = [str(tx) for tx in new_block['transactions']]

        # Hash the JSON representation of the new block
        _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()

        # keep hashing the block until the hash meets the required difficulty
        while _hash > self.hash_difficulty:
            if not self.reset_mine_function:  # keep hashing unless a new block was received
                new_block['nonce'] += 1
                _hash = hashlib.sha256(json.dumps(new_block).encode()).hexdigest()
                print(_hash)
            else:  # if a new block was received, break and exit the function, returning an empty string (falsy)
                _hash = ''
                break

        if _hash: # finished mine function uninterrupted, successfully mined new block
            print('found correct hash')
            new_block['hash'] = _hash
            new_block_json = json.dumps(new_block)
            # clear mined transactions from queue
            self.transaction_queue = [x for x in self.transaction_queue if x not in transactions]
            return new_block_json  # this string will be sent to other nodes
        else: # mine function interrupted, returning empty string.
            return _hash

    def send_msg(self, contents: str, type: str):
        """
        sends msgs to all peers

        :param contents: str. Newly mined blocks or new transactions in JSON string representation.
        :param type: str. indicates type of msg. 'Block' or 'Transaction'
        :return: None
        """
        # send block to all known peers
        msg_dict = {'contents': contents, 'type': type}
        for peer in self.peers:
            self.messenger.send(msg_dict, peer)

if __name__ == '__main__':
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



    n = Node('0')
    sleep(3)
    print('****************************************************\n'*3)
    n.handle_incoming_message({'type': 'Transaction', 'contents': str(Transaction(_to='node1', _from='node3', amount=1))})
    n.handle_incoming_message({'type': 'Transaction', 'contents': str(Transaction(_to='node3', _from='node1', amount=.9))})
    print('-----------------------------------------------------\n'*3)
    sleep(3)
    #  n.handle_incoming_message({'type' : 'Block', 'contents' : new_block_json})
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n'*3)
    # sleep(3)
    n.stop_mine_function=True
    print(n.blockchain)
    print('transaction list: ', n.transaction_queue)