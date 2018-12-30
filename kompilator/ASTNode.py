class ASTNode:
    def __init__(self, value=None, children=[]):
        self.children = children
        self.value = value