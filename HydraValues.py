class HydraValues:
    def __init__(self):
        self.column1 = "Common"
        self.column2 = "Uncommon"
        self.column3 = "Rare"
        self.column4 = "Legendary"

        self.herpderp = [
            [25, 40, 70, 150],
            [35, 50, 85, 190],
            [40, 65, 110, 280],
        ]
        
    def getvalue(self, x, y):
        return self.herpderp[y][x]