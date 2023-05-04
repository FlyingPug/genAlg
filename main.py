import random

TARGET_COLOR = [96, 96, 159]
START_POPULATION = 200
PROB_OF_CROSS = 0.5


def gen_color():
    return [random.randint(0, 255) for _ in range(3)]


def fit(color):
    return sum(abs(color[i] - TARGET_COLOR[i]) for i in range(3))


def roulette_wheel_pop(population, probabilities, number):
    chosen = []
    for n in range(number):
        r = random.random()
        prob_circle = 0
        for i in range(len(probabilities)):
            prob_circle += probabilities[i]
            if r <= prob_circle:
                chosen.append(population[i])
                break
    return chosen


def to_binary(individual):
    return "{0:b}".format(individual[0]).zfill(8) + "{0:b}".format(individual[1]).zfill(8) + "{0:b}".format(
        individual[2]).zfill(8)


def to_decimal(individual):
    return [int(individual[:8], 2), int(individual[8:16], 2), int(individual[16:], 2)]


def pop_to_binary(population):
    binary_pop = []
    for individual in population:
        binary_pop.append(to_binary(individual))
    return binary_pop


def pop_to_decimal(population):
    decimal_pop = []
    for individual in population:
        decimal_pop.append(to_decimal(individual))
    return decimal_pop


def crossover(parent_1, parent_2):
    return parent_1[:12] + parent_2[12:]

def crossover_rand(parent_1, parent_2):
    split = random.randint(1, 15)
    return parent_1[:split] + parent_2[split:]

def get_uniq_individual(population):
    new_population = []
    for elem in population:
        if elem not in new_population:
            new_population.append(elem)
    return new_population


def mutation(individual):
    prob_of_mutation = (1 / len(individual))
    result = ''
    for digit in individual:
        if random.random() >= prob_of_mutation:
            result += '1' if digit == '0' else '0'
        else:
            result += digit
    # for i in range(1, 4):
    #    index = random.randint(8 * (i-1), 8 * i - 1)
    #    result = result[:index] + ('1' if result[index] == '0' else '0') + result[index + 1:]
    return result


def population_crossover(population):
    new_pop = []
    for i in range(0, len(population), 2):
        if PROB_OF_CROSS > random.random():
            new_pop.append(mutation(crossover_rand(population[i], population[i + 1])))
            new_pop.append(mutation(crossover_rand(population[i + 1], population[i])))
        else:
            new_pop.append(population[i])
            new_pop.append(population[i + 1])
    return new_pop


result_population = []
for i in range(START_POPULATION):
    result_population.append(gen_color())
for j in range(1000):
    population_fitness = []
    for i in range(len(result_population)):
        fitness = fit(result_population[i])
        population_fitness.append(fitness)
    # fitness prob
    fitness_prob = []
    for i in range(len(population_fitness)):
        prob = population_fitness[i] / sum(population_fitness)
        fitness_prob.append(prob)
    population_for_crossover = roulette_wheel_pop(result_population, fitness_prob, START_POPULATION)
    binary_population_for_crossover = pop_to_binary(population_for_crossover)

    new_population = population_crossover(binary_population_for_crossover)
    # to decimal
    population_for_crossover = get_uniq_individual(population_for_crossover)
    new_population = pop_to_decimal(new_population)

    population_for_crossover.sort(key=fit, reverse=True)
    new_population.sort(key=fit, reverse=True)
    result_population = population_for_crossover[:6] + new_population[6:]

    if result_population[0] == TARGET_COLOR:
        break
print(f'Последняя популяция № {j}')
print(result_population)
for i in range(len(result_population)):
    print(f'Цвет особи #{i} равн {result_population[i]}, а ее приспособленность - {fit(result_population[i])}')
