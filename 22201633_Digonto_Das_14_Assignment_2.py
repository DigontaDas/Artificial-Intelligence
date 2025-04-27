import random
def initial_population(size):
    lst=[]
    while len(lst)<size:
        loss=random.randint(1,99)
        profit=random.randint(1,99)
        trade=random.randint(1,99)
        if profit>loss:
            lst.append(chromo(loss,profit,trade))
        
    return lst

#ei functione pathai dictonary theke string ta ke alada kortese
def modifying_chromosome(chromosome):
    populated_chromosome=""
    for first,second in chromosome.items():
        if len(str(second)) == 2:
            populated_chromosome+=str(second)
        else:
            populated_chromosome+= "0" +str(second)
    return populated_chromosome

#dictionary create kortese
def chromo(stop_loss,take_profit,trade_size):
    new={
        "stop loss" : stop_loss,
        "take profit": take_profit,
        "trade size" : trade_size,
    }
    return new

#fitness check kortese prottek generation er jonno and oikhane notun capital theke puran ta baad diche
def fitness(initial_capital, chromosome,price_changes):
    populated_chr=modifying_chromosome(chromosome)
    loss = int(populated_chr[:2])
    profit = int(populated_chr[2:4])
    trade= int(populated_chr[4:])
    new_capital=initial_capital 
    for i in price_changes:
        Updated_Capital = (new_capital * trade) / 100
        new_capital -= Updated_Capital
        if i > -(loss) and i < profit:
            Updated_Capital += (Updated_Capital * i) / 100
        else:
            if i < 0:
                Updated_Capital += (Updated_Capital * loss) / 100
            else:
                Updated_Capital += (Updated_Capital * profit) / 100
        new_capital += Updated_Capital

    return new_capital - initial_capital

def crossover(parent_chromo):
    #ekta random point nicche and oi point theke bhangtese and ekta list e dhukai raktese
    point = random.randint(1, 5)
    x1, x2 = parent_chromo[0], parent_chromo[1]
    offspring1 = x1[:point] + x2[point:]
    offspring2 = x2[:point] + x1[point:]
    return [offspring1,offspring2]

def mutation(crossed_springs):
    new_offsprings=[]
    rate=.05
    for mutated in crossed_springs:
        if len(mutated) < 6:
            # generate kortese random chromosome jodi invalid hoi
            stop_loss = f"{random.randint(1,99):02d}"
            profit = f"{random.randint(1,99):02d}"
            trade = f"{random.randint(1,99):02d}"
            chromosome = stop_loss + profit + trade
            new_offsprings.append(chromosome)
            
        #prottek part alada kortese
        stop_loss,profit,trade=(mutated[0:2]),(mutated[2:4]),(mutated[4:])
        #prottek part er jonno rate check kore change kortese
        if random.random()< rate:
            mutation=(random.choice(['stop_loss','profit','trade']))
            if mutation=='stop_loss':
                stop_loss=f"{random.randint(1,99):02d}"
            elif mutation=='profit':
                profit=f"{random.randint(1,99):02d}"
            elif mutation=='trade':
                trade=f"{random.randint(1,99):02d}"
        chromosome=(stop_loss)+(profit)+(trade)
        #profit boro hobe loss theke
        if int(profit)>int(stop_loss):
            new_offsprings.append(chromosome)

    return new_offsprings

def genetic_algo(initial_capital,price_changes,population_size, generations):
    fill_population = initial_population(population_size)
    best_profit=0
    best_chromosome = None
    for generation_count in range(generations): 
        ideal_chromosomes={}
        #ekbar kore generations nicche and fitness check kore pathacche then dictionary r moddhe store kortesi after modifying 
        for chromosome in fill_population:
            best_profit=fitness(initial_capital,chromosome,price_changes)
            ideal_chromosomes[best_profit]=modifying_chromosome(chromosome)

        sort_chromo = sorted(ideal_chromosomes.keys(),reverse=True) #reverse e sort e ekta list return kortese
        # selects random 2 for crossover reverse korar por
        index=random.randint(0, len(ideal_chromosomes) - 1)
        best_chromo_lst = [ideal_chromosomes[sort_chromo[index]], ideal_chromosomes[sort_chromo[index]]]

        # best chromosome track kortese
        if sort_chromo[0] > best_profit:
            best_profit = sort_chromo[0]
            best_chromosome = ideal_chromosomes[sort_chromo[0]]

        offsprings = crossover(best_chromo_lst)
        mutated_offsprings = mutation(offsprings)
 
        #notun population generate kortese
        new_population=[]
        for i in mutated_offsprings:
            if len(i) ==6:
                stop_loss=int(i[:2])
                profit=int(i[2:4])
                trade=int(i[4:])
                if profit>stop_loss:
                    new_population.append(chromo(stop_loss,profit,trade))
    if best_chromosome==None: #majhe majhe None ashtesilo tai 
        print("Coundnt Find Chromosome")
    return best_chromosome, best_profit


starting_capital = 1000
population = 4
generations = 10
price_changes = [-1.2, 3.4, -0.8, 2.1, -2.5, 1.7, -0.3, 5.8, -1.1, 3.5]

result = genetic_algo(starting_capital, price_changes, population, generations)
print("Best Strategy:")
print(f"Stop Loss: {int(result[0][:2])}, Take Profit: {int(result[0][2:4])}, Trade Size: {int(result[0][4:])}")
print("Final Profit:", result[1])

#############################  PART 2   #############################################################

def two_point_crossover(parent_1, parent_2):
    length_parent=len(parent_1)
    # Ensure that two crossover points are distinct and in the correct order
    p1, p2 = sorted(random.sample(range(1, length_parent), 2))
    
    off_spring_1 = parent_1[:p1] + parent_2[p1:p2] + parent_1[p2:]
    off_spring_2 = parent_2[:p1] + parent_1[p1:p2] + parent_2[p2:]
    
    return [off_spring_1,off_spring_2]
parent_1 = "000111000"
parent_2 = "111000111"
off_springs=two_point_crossover(parent_1,parent_2)
print(f"Parent-1:{parent_1}\nParent-2:{parent_2}\nOffspring-1: {off_springs[0]}\nOffspring-2: {off_springs[1]}")

