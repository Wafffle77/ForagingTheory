import random

class FoodBag:
    def __init__(self, containedEnergy):
        self.containedEnergy: float = containedEnergy

class Animal:
    def __init__(self, extractionThreshold, initialEnergy):
        self.extractionThreshold: int = extractionThreshold
        self.energy: float = initialEnergy

class World:
    def __init__(self, animals, bags, bagWeights, bagNumber, searchCost, extractionCost):
        self.animals: list[Animal]   = animals
        self.bags: list[FoodBag]     = bags
        self.bagAmounts: list[int]   = bagWeights
        self.searchCost: float       = searchCost
        self.extractionCost: float   = extractionCost
    
    def getBag(self):
        totalBags = sum(self.bagAmounts)
        if totalBags <= 0:
            return None
        

        return random.choices(self.bags, self.bagWeights, self.bagNumber)
    
    def step(self):
        # Ensure the same animals aren't always getting the first pick
        random.shuffle(self.animals)

        for animal in self.animals:
            
