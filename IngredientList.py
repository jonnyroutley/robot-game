from random import shuffle

class IngredientList:
    # intention here is to help improve how new ingredients are generated
    # this class uses a factor to create an array with *factor* times more good ingredients than bad
    # the array is then shuffled, and items can be taken from this shuffled array

    def __init__(self, factor, I_NUMS_GOOD, I_NUMS_BAD):
        self.factor = factor

        # exclude base from this 
        self.items = I_NUMS_GOOD[1:] * factor + I_NUMS_BAD
        shuffle(self.items)