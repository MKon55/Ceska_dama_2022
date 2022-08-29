class Node:
    def __init__(self, parent, data, turnChange, killedPiece):
        self.parent = parent
        self.children = []
        self.data = data
        self.turnChange = turnChange
        self.killedPiece = killedPiece

    def AddChild(self, child):
        self.children.append(child)

    def RemoveChild(self, child):
        self.children.remove(child)
