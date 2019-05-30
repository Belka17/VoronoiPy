class Point:
    def __init__(self, x="", y=""):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return abs(self.x - other.x) < 0.00001 and abs(self.y - other.y) < 0.00001

    def __ne__(self, other):
        x = self == other
        return not x
