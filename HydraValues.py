class HydraValues:
    hydraNames = [
        "Common", "Elder", "Ancient", "Dreadful"
    ]

    scoreTableHydraNameHeadValue = [
        [25, 40, 70, 150],
        [35, 50, 85, 190],
        [40, 65, 110, 280],
        [45, 665, 120, 280],
        [50, 765, 150, 280],
        [80, 800, 170, 999],           
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