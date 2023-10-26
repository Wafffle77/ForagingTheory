import random, math, os
from copy import copy

def average(iter): return sum(iter) / len(iter)

class FoodBag:
    def __init__(self, containedEnergy, containedDuds, valuePerEnergy):
        self.containedEnergy: int = containedEnergy
        self.containedDuds: int = containedDuds
        self.valuePerEnergy: float = valuePerEnergy
    
    def sample(self, number: int):
        sampleList = [1 for i in range(self.containedEnergy)] + [0 for i in range(self.containedDuds)]
        random.shuffle(sampleList)
        return sampleList[:int(number)]

class Animal:
    def __init__(self, extractionThreshold, initialEnergy = 0.0):
        self.extractionThreshold: int = extractionThreshold
        self.energy: float            = initialEnergy

class World:
    def __init__(self, animals, bags, bagWeights, bagNumber, searchCost, extractionCost):
        self.animals: list[Animal]   = animals
        self.originalAnimals: list[Animal] = copy(animals)
        self.searchCost: float       = searchCost
        self.extractionCost: float   = extractionCost

        self.bags: list[FoodBag]     = random.choices(population=bags, weights=bagWeights, k=bagNumber)
    
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
            if not bag:
                return True
            
            # print(animal.energy)
            animal.energy -= self.searchCost
            if any(bag.sample(animal.extractionThreshold)):
                animal.energy += bag.containedEnergy * bag.valuePerEnergy - self.extractionCost * (bag.containedDuds + bag.containedEnergy)
            else:
                animal.energy -= animal.extractionThreshold * self.extractionCost
            # print(animal.energy)
        
        return False
    
    def run(self):
        while not self.step(): pass
    
    def runDebug(self):
        with open("animals.csv.tmp", "w") as logFile:
            for a in self.originalAnimals:
                logFile.write(f"{a.extractionThreshold},")
            logFile.write("\n")
            while not self.step():
                for i, a in enumerate(self.originalAnimals): 
                    # print(f"{i}:\t{a.extractionThreshold}\t{a.energy}")
                    logFile.write(f"{a.energy},")
                logFile.write("\n")

class LearningWorld():
    def __init__(self, iterations, noise, initialExtractionThreshold, animalNumber, bags, bagWeights, bagNumber, searchCost, extractionCost):
        self.iterations     = iterations
        self.noise          = noise
        self.extractionThreshold = initialExtractionThreshold
        self.animalNumber   = animalNumber
        self.bags           = bags
        self.bagWeights     = bagWeights
        self.bagNumber      = bagNumber
        self.searchCost     = searchCost
        self.extractionCost = extractionCost
    
    def learn(self):
        for i in range(self.iterations):
            animals = [Animal(math.floor(self.extractionThreshold + (random.random() - 0.5) * self.noise + 0.5)) for i in range(self.animalNumber - 1)]
            animals.append(Animal(self.extractionThreshold))
            world = World(animals, self.bags, self.bagWeights, self.bagNumber, self.searchCost, self.extractionCost)
            if self.iterations == i + 1:
                world.runDebug()
            if i == 0:
                world.runDebug()
                os.system("MOVE animals.csv.tmp animals0.csv")
            else:
                world.run()
            yield world

            self.extractionThreshold = max(world.animals, key=lambda a: a.energy).extractionThreshold

bags       = [FoodBag(20 - i, i,3) for i in range(20)]
bagWeights = [0.05 for i in range(20)]
bagNumber  = 1024

learn = LearningWorld(
    256,             # Iterations
    2,               # Noise
    3,               # Extraction Threshold
    16,              # Number of Animals
    bags,            # List of bags
    bagWeights,      # Weights of bags 
    bagNumber,       # Number of bags
    5,               # Search Cost
    1                # Extraction Cost
)

for world in learn.learn():
    world.animals.sort(key=lambda a: a.energy)
    print(
        int(average([a.energy for a in world.animals])),
        world.animals[0].extractionThreshold,
        world.animals[0].energy,
        world.animals[-1].extractionThreshold,
        world.animals[-1].energy,
        sep='\t'
    )

os.system("MOVE animals.csv.tmp animals.csv")