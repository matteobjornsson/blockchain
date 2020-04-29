
class BlockChain:
    last_block = None # represents the block with longest chain length
    branches = [] # list of pointer pairs defining branches: tip & fork, first entry = tip and genesis
    chain = None #NumpyArray

    def __init__(self):
        filename = ''
        blocks = []
    def process_block(self, block) -> bool:
        # verify proof of work
        # verify transactions -> self.ledger.verifytx(block.tx)
        # if both pass, add block to chain
        pass

    def add_block(self):
        # append to array
        # look at all branch tips
        #   if tip hash matches prev hash of incoming block,
        #       update tip pointer of that branch to self
        #       update global chain length counter and last block if now longest
        #       update corresponding branch ledger
        #   else if incoming block position within n blocks of longest branch
        #      self = new branch (tip and fork point to self hash)
        #      create new branch ledger
        # check for trim
        pass

    def trim_chain(self):
        # for each branch in branches
        #   compare position of tip to longest chain counter, if more than n behind, delete branch
        pass

    def delete_branch(self, tip, fork):
        # traverse branch from tip to fork and delete all blocks up to fork. Hopefully numpy array takes care of reorganizing array)
        pass

    def add_branch(self, hashOfBlockToAdd):
        # add pair of pointers to branch list, both tip and fork with same value
        pass

    def get_last_block(self):
        return self.last_block

