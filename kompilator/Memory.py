class MemoryException(Exception):
    pass


class MemoryManager:
    def __init__(self):
        self.memmap = {}
        self.lastblockid = 0

    def assignMem(self, declaration=None):
        assignedMemoryBlockId = self.lastblockid

        if declaration:
            name = declaration.pidentifier
            if name in self.memmap:
                return self.memmap[name]
            declaration.memoryId = assignedMemoryBlockId
            self.memmap[name] = assignedMemoryBlockId

        self.lastblockid += 1
        return assignedMemoryBlockId

    def getBlockId(self, name):
        if not name in self.memmap:
            raise MemoryException("Identifier %s has no memory allocated" % name)
        return self.memmap[name]


manager = MemoryManager()