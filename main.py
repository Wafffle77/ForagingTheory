import random

class FoodBag:
    def __init__(self, containedEnergy, containedDuds):
        self.containedEnergy: int = containedEnergy
        self.containedDuds: int = containedDuds
    
    def sample(self):
        return

class Animal:
    def __init__(self, extractionThreshold, initialEnergy):
        self.extractionThreshold: int = extractionThreshold
        self.energy: float = initialEnergy

class World:
    def __init__(self, animals, bags, bagWeights, bagNumber, searchCost, extractionCost):
        self.animals: list[Animal]   = animals
        self.searchCost: float       = searchCost
        self.extractionCost: float   = extractionCost

        self.bags: list[FoodBag]     = random.choices(bags, bagWeights, bagNumber)
    
    def getBag(self):
        try:
            return self.bags.pop()
        except IndexError:
            return None
    
    def step(self):
        # Ensure the same animals aren't always getting the first pick
        random.shuffle(self.animals)

        for animal in self.animals:
            bag = self.getBag()
            weights = [random]
