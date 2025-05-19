class HydraValues:
    hydraNames = [
        "Common", "Elder", "Ancient", "Dreadful"
    ]

    scoreTableHydraNameHeadValue = [
        [25, 40, 70, 150],
        [35, 50, 85, 190],
        [40, 65, 110, 280],
        [50, 80, 180, 340],
        [65, 140, 210, 430],
        [120, 210, 290, 590],           
    ]

    @staticmethod
    def getHydraIndex(hydra_name, rowIndex):
        index = HydraValues.hydraNames.index(hydra_name)
        rowIndex = min(rowIndex, len(HydraValues.scoreTableHydraNameHeadValue) - 1)
        return HydraValues.scoreTableHydraNameHeadValue[rowIndex][index]


    @staticmethod
    def TableValues():
        return HydraValues.scoreTableHydraNameHeadValue

    @staticmethod
    def ListOfHydraNames():
        return HydraValues.hydraNames