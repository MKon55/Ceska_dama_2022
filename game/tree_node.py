class Node:
    def __init__(self, parent, data, turnChange, killedPiece, forced, move=None):
        self.parent = parent
        self.children = []
        self.data = data
        self.turnChange = turnChange
        self.killedPiece = killedPiece
        self.forced = forced
        self.move = move

    def AddChild(self, child):
        self.children.append(child)

    def RemoveChild(self, child):
        self.children.remove(child)
