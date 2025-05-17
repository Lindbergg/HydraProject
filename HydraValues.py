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
        # Get the index of the hydra name
        index = HydraValues.hydraNames.index(hydra_name)
        # Get the value from the score table
        value = HydraValues.scoreTableHydraNameHeadValue[rowIndex][index]
        # Return the value as a string
        return str(value)


    @staticmethod
    def TableValues():
        return HydraValues.scoreTableHydraNameHeadValue

    @staticmethod
    def ListOfHydraNames():
        return HydraValues.hydraNames