import random

class FoodBag:
    def __init__(self, containedEnergy, containedDuds):
        self.containedEnergy: int = containedEnergy
        self.containedDuds: int = containedDuds

class Animal:
    def __init__(self, extractionThreshold, initialEnergy):
        self.extractionThreshold: int = extractionThreshold
        self.energy: float = initialEnergy

class World:
    def __init__(self, animals, bags, bagWeights, bagNumber, searchCost, extractionCost):
        self.animals: list[Animal]   = animals
        self.searchCost: float       = searchCost
        self.extractionCost: float   = extractionCost

        self.bags: list[FoodBag]     = bags
        self.bagWeights: list[int]   = [int(bagWeight * bagNumber) for bagWeight in bagWeights]
        self.bagNumber: int          = bagNumber
    
    def getBag(self):
        if self.bagNumber <= 0:
            return None
        
        return random.choices(self.bags, self.bagWeights)
    
    def step(self):
        # Ensure the same animals aren't always getting the first pick
        random.shuffle(self.animals)

        for animal in self.animals:
            
