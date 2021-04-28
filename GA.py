import random
import math
import time

start_time = time.time()

crossoverprop = 0.05
mutprob = 0.2
numpop = 100
stagmax = 10
convergence = 10
elitism = 2
geneticDist = 0

fitshare = False

Genalpha = 2
Gensigma = 5

mu = 25
sigma = 5

print('Select number of generations:')
gennum = int(input())
print('Select Target')
optimum = float(input())

pop = []
stag = []
best = []

pop_plot = []

for i in range(0, numpop):
    pop.append(random.gauss(mu, sigma))
    stag.append(0)


# crossover

def rand(num1, num2):
    return random.uniform(num1, num2)


def geomean(num1, num2):
    if (num1 * num2) < 0:
        return -(abs(num1 * num2) ** 0.5)
    else:
        return (num1 * num2) ** 0.5


def mean(num1, num2):
    return (num1 + num2) / 2


# mutation

def addmut(num):
    return num + random.gauss(0, 20)


def divmut(num):
    return num / abs(random.gauss(0, 10))


def multmut(num):
    return num * abs(random.gauss(0, 10))


def expmut(num):
    exp = random.gauss(1, 0.5)
    if num < 0:
        return -(abs(num)) ** exp
    else:
        return num ** exp


crossops = [rand, geomean, mean]
mutops = [addmut, divmut, multmut, expmut]


# fitness

def OptFuction(target, num):
    return 2*math.sin(0.25*math.pi*num)+(0.25*num)**2

def Share(Ind1, Ind2, alpha, sigma):
  if (Ind1-Ind2)**2 <= sigma:
    return (1-(Ind1-Ind2)**2)**alpha
  else:
    return 0

def FitShare(population, fitlist):
  for individual1 in range(len(population) ):
    shfitsum = []
    for individual2 in range(len(population) ):
      shfitsum.append(Share(individual1, individual2, Genalpha, Gensigma))
      
    fitlist[individual1] = sum(shfitsum)

for generation in range(gennum):
    
    print(f'Running Generation {generation + 1}')
    
    fitness = []
    rankedfit = []
    crossover = []

    prevlen = len(pop)

    for member in pop:
        fitness.append(OptFuction(optimum, member))
		
    for newmember in pop[prevlen:]:

        fitness.append(OptFuction(optimum, newmember))
    
    if fitshare == True:
    	
      FitShare(pop, fitness)

    print(len(pop))
    print(len(fitness))
    print(len(stag))
		
    poptemp = []
    stagtemp = []
    fittemp = []
		
    for stagnation in range(len(stag)):

        if stag[stagnation] < stagmax:
            
            poptemp.append(pop[stagnation])
            stagtemp.append(stag[stagnation])
            fittemp.append(fitness[stagnation])
        
        else:
          print(f'Individual {pop[stagnation]} with stagnation {stag[stagnation]} went extinct.')

    stag = stagtemp
    fitness = fittemp
    pop = poptemp
		
    for stagnation in range(len(stag)):
        stag[stagnation] += 1

    rankedfit = sorted(fitness)

    for mutsubj in range(len(pop)):
        if random.uniform(0, 1) < mutprob:
            if random.uniform(0, 1) < (rankedfit[rankedfit.index(fitness[mutsubj])]) ** elitism:
                prev = pop[mutsubj]
                pop[mutsubj] = random.choice(mutops)(pop[mutsubj])
                if OptFuction(optimum, pop[mutsubj]) < OptFuction(optimum, prev):
                    stag[pop.index(pop[mutsubj])] = 0

    if (len(rankedfit) * crossoverprop) % 1 != 0:
        if math.floor(len(rankedfit) * crossoverprop) % 2 == 0:
            crossover.extend(rankedfit[0:math.floor(len(rankedfit) * crossoverprop)])
        else:
            crossover.extend(rankedfit[0:math.ceil(len(rankedfit) * crossoverprop)])
    else:
        if len(rankedfit) * crossoverprop * crossoverprop % 2 == 0:
            crossover.extend(rankedfit[0:int(len(rankedfit) * crossoverprop)])
        else:
            crossover.extend(rankedfit[0:int(len(rankedfit) * crossoverprop + 1)])

    crosstemp = crossover
    crossover = []

    for fit in crosstemp:
        crossover.append(pop[fitness.index(fit)])

    random.shuffle(crossover)

    crosstemp = crossover
    crossover = []

    ind = 0
    while ind <= len(crosstemp) - 2:
        crossover.append(crosstemp[ind:ind + 2])
        ind += 2

    for couple in crossover:
        pop.append(random.choice(crossops)(couple[0], couple[1]))
        stag.append(0)
        stag[pop.index(couple[0])] = 0
        stag[pop.index(couple[1])] = 0

    print(pop)

    fitness = []

    for member in pop:
        fitness.append(OptFuction(optimum, member))

    best.append(pop[fitness.index(min(fitness))])

    if len(set(best[len(best) - convergence:])) == 1 and generation > convergence:
        print(best)
        print(f'Convergence threshold of {convergence} reached, terminating.')
        break

    pop_plot.append(pop)

    print(f'Best Individual: {pop[fitness.index(min(fitness))]} out of a popultation of {len(pop)}')
    
    import matplotlib.pyplot as plt
    plt.plot(best)
    plt.show
