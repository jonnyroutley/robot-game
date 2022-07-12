class Ingredient:
    def __init__(self, kind, I_NAMES, x = 0, y = 0):
        self.x = x
        self.y = y
        self.kind = kind            # a number which corresponds to the kind of ingredient
        self.name = I_NAMES[kind]   # the string that corresponds the the number kind
        self.collected = False
        self.is_good = True if kind % 2 == 0 else False # whether or not this ingredient is good to eat