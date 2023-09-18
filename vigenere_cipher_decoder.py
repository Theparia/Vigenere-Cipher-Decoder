import string, time, re, random

POPULATION_SIZE = 500
CROSSOVER_RATE = 0.8
CARRY_RATE = 0.1

POPULATION_SIZE = 500
CROSSOVER_RATE = 0.8
CARRY_RATE = 0.1

class Decoder:   
    def __init__(self, globalText, encodedText, keyLength):
        self.encodedText = encodedText
        self.encodedWords = self.cleanData(self.encodedText.lower())
        self.dictionary = set(self.cleanData(globalText.lower()))
        self.keyLength = keyLength
        
    def cleanData(self, data):
        data = re.sub(r'[^A-Za-z]', ' ', data)
        return data.split()
    
    def decode(self):
        population = self.makeFirstPopulation()
        
        while True:
            population = self.sortByFitness(population)
#             print('best fitness: ', self.calcFitness(population[POPULATION_SIZE - 1]), 'best key: ', population[POPULATION_SIZE - 1])

            if self.calcFitness(population[POPULATION_SIZE - 1]) == len(self.encodedWords):
                self.correctKey = population[POPULATION_SIZE - 1]
                print('Key: ', self.correctKey)
                return self.decodeWithKey(self.correctKey)

            population = self.rankBasedSelection(population)
            children = self.crossoverOnPopulation(population)
            children = self.mutateOnChildren(children)
            population = children
    
    def makeFirstPopulation(self):
        return [self.makeRandomChromosome() for i in range(POPULATION_SIZE)]
     
    def makeRandomChromosome(self):
        alphabet = list(string.ascii_lowercase)
        key = ''
        for i in range(self.keyLength):
            key += random.choice(alphabet)
        return key
    
    def sortByFitness(self, population):
        return sorted(population, key = lambda p: self.calcFitness(p))
    
    def calcFitness(self, chromosome):
        decipheredWords = self.decodeWordsWithKey(chromosome)     
        counter = 0
        for word in decipheredWords:
            if word in self.dictionary:
                counter += 1    
        return counter

    def decodeWithKey(self, key):
        originalText = []
        j = 0
        for i in range(len(self.encodedText)):
            if self.encodedText[i] in string.ascii_letters:
                x = (ord(self.encodedText[i].lower()) - ord(key[j % self.keyLength].lower()) + 26) % 26
                j += 1
                if self.encodedText[i].islower():
                    x += ord('a')
                else:
                    x += ord('A') 
                originalText.append(chr(x))
            else:
                originalText.append(self.encodedText[i])
                               
        return(''.join(originalText)) 
    
    def decodeWordsWithKey(self, key):
        decipheredWords = []
        i = 0
        for word in self.encodedWords:    
            temp = ''
            for char in word:
                x = (ord(char) - ord(key[i % self.keyLength]) + 26) % 26
                x += ord('a')
                temp += chr(x)
                i += 1
            decipheredWords.append(temp)
        return decipheredWords
    
    def rankBasedSelection(self, population): 
        matingPool = []
        for i in range(int((1 - CARRY_RATE) * POPULATION_SIZE), POPULATION_SIZE):
            matingPool.append(population[i])
        accumulated = []
        sum_rank = POPULATION_SIZE * (POPULATION_SIZE + 1) / 2
        accumulated = [(i * (i + 1) / 2)/sum_rank for i in range (1, POPULATION_SIZE + 1)]        
        while len(matingPool) < POPULATION_SIZE:
            r = random.random()
            for j in range(len(accumulated)):
                if accumulated[j] >= r:
                    matingPool.append(population[j]);
                    break                
        return matingPool
    
    def mutateOnChildren(self, children):
        for i in range(len(children)):
            children[i] = self.mutate(children[i])
        return children
    
    def mutate(self, chromosome):
        chromosome = list(chromosome)
        index = random.randint(0, self.keyLength - 1)
        char = random.choice(list(string.ascii_lowercase))
        chromosome[index] = char
        return ''.join(chromosome)
    
    def crossoverOnPopulation(self, population):
        children = []
        while len(children) < len(population):
            r = random.uniform(0, 1)
            parent1 = random.choices(population)[0]
            parent2 = random.choices(population)[0]
            if r < CROSSOVER_RATE:
                child1, child2 = self.crossover(parent1, parent2)
                children.append(child1)
                children.append(child2)
            else:
                children.append(parent1)
                children.append(parent2)
        return children
    
    def crossover(self, parent1, parent2):
        child1 = list(parent1)
        child2 = list(parent2)
        point = random.randint(1, self.keyLength - 2)
        for i in range(point, self.keyLength):
            child1[i] = parent2[i]
            child2[i] = parent1[i]  
        return ''.join(child1), ''.join(child2)

encodedText = open('test.txt').read()
globalText = open('global_text.txt').read()

d = Decoder(globalText, encodedText, 14)

start = time.time()
decodedText = d.decode()
end = time.time()

print("Time: %s seconds" % (end - start) , "\n")
print("The decoded text is: \n")
print(decodedText)