class MemoryException(Exception):
    pass


class MemoryManager:
    def __init__(self):
        self.memmap = {}
        self.lastblockid = 0

    def assignMem(self, name):
        if name in self.memmap:
            raise MemoryException(name)
            return self.memmap[name]
        assignedMemoryBlockId = self.lastblockid
        self.memmap[name] = assignedMemoryBlockId
        self.lastblockid += 1
        return assignedMemoryBlockId