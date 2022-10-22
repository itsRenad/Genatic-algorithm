import random
import matplotlib.pyplot as plt

Scontainer = "container"
Sitem = "item"

class SmartCargoLoading:
    #Add the items to the containers
    def Add(self, container, item, opt, Chromo):
        weight=0
        if opt == 1:
            weight = item / 2
        elif opt == 2:
            weight = (item ** 2) / 2
        Chromo[container].append((Sitem + str(item), weight))
    
    def Find_Weight_Diff(self, pop):
        #list to store the sum of weights in each container
        sum_weights = []
        #iterating over the dictionary containing container and weights and calculating the sum of weights in each container
        for _, value in pop.items():
            summ = 0
            #as we have (item,weight) tuple 
            for (_,weight) in value:
                #adding up weights in each container
                summ += weight
            #adding summed weights to list
            sum_weights.append(summ)
        max_weight = max(sum_weights)
        min_weight = min(sum_weights)
        return max_weight - min_weight
    
    """creates n number of random populations"""
    def Create_Populations(self,num,items, containers, option):
        Population = []
        while num > 0:
            Population.append(self.Create_Random_Population(items, containers, option))
            num -= 1
        return Population
    
    """creates a random chromosome, which is randomly adds items to the containers"""
    def Create_Random_Population(self, items, containers, option):
        Chromosome={}
        for i in range(1, containers + 1):
            # Perparing the containers name to be as  container1,container2...
            ContainerName = Scontainer + str(i)
            Chromosome[ContainerName] = []
        # Store the number of the items
        i = items
        while i > 0:
            # To distribute the items randomly generate a value between 1 and 2
            prob = random.randint(1, 2)
            d = list(Chromosome)
            if prob > 1:
                # Chose a container in even index
                rand = random.randrange(0, containers, 2)
                # Add the item to the even container
                self.Add(d[rand], i, option, Chromosome)
            # if prob value is greater than 1
            else:
                # Chose a container in odd index
                rand = random.randrange(1, containers, 2)
                # Add the item to the odd container
                self.Add(d[rand], i, option, Chromosome)
            i -= 1
        return Chromosome
    
    """calculates fitness of a given chromosome"""
    def Calculate_Fitness(self,chromosome):
        fit = self.Find_Weight_Diff(chromosome)
        return fit
    
    """calculates fitness of all the chromosomes in the population"""
    def All_Fitness(self,pop):
        fitness = []
        for chrom in pop:
            fitness.append(self.Calculate_Fitness(chrom))
        return fitness
    
    def Single_Point_Crossover(self,randPopA, randPopB):
        """this function performs the single point cross over at a random selected point within the categories."""
        point = random.randint(1, len(randPopA)-1)
        i = 0
        aa = []
        bb = []
        l1 = list(randPopA.items())
        l2 = list(randPopB.items())
        while i != point:
            aa.append(l1[i])
            bb.append(l2[i])
            i += 1
        while i < len(randPopA):
            aa.append(l2[i])
            bb.append(l1[i])
            i += 1
        aa = dict(aa)
        bb = dict(bb)
        return aa, bb
    
    def Mutate(self,pop, randPopA, PhenotypeMutationRate):
        '''This function performs mutation on the population. The initial mutation rate is first selected that 
        is the phenotype mutation rate. 
        then a genotype mutation rate is selected. if that G_mutation rate is less than P_mutation rate, then the 
        genotype gets swapped. '''
        pop1 = list(randPopA.items())
        pop2 = list(pop.items())
        i=random.randint(0,len(randPopA)-1)
        GenemutationR = random.uniform(0, 1)
        if GenemutationR < PhenotypeMutationRate:
            pop1[i] = pop2[i]
        return dict(pop1)
    
    """creates a random population and mutates the given population with the random population"""
    def Start_Mutation(self,randPopA, randPopB, items,containers):
        rand = random.uniform(0,1)
        randomPoP = None
        #creating a random population to mutate the population with. 
        if rand > 0.5:
            randomPoP = self.Create_Random_Population(items, containers,"A")
        else:
            randomPoP = self.Create_Random_Population(items, containers,"B")
        #mutating both of the population
        randPopA = self.Mutate(randomPoP, randPopA, random.uniform(0, 1))
        randPopB = self.Mutate(randomPoP, randPopB, random.uniform(0, 1))
        return randPopA, randPopB
    
    """returns the two best fitness valued chromosomes from the population
        which is the chromosome whose weight difference between the heaviest and lightest
        container is minimum"""
    def Ellitist_Wheel_Selection(self,fitness,Population):
        for i in range(0,len(fitness)):
            for j in range(0,len(fitness)-i-1):
                if fitness[j] > fitness[j+1]:
                    temp = fitness[j]
                    temp1 = Population[j]
                    fitness[j] = fitness[j+1]
                    Population[j] = Population[j+1]
                    fitness[j+1] = temp
                    Population[j+1] = temp1
        return Population[0],Population[1],fitness
    
    """This function is used to add the newly created random chromosomes to the population
        This function works in a way that it first adds the chromosomes and their fitness values to the 
        population and fitness. It then sorts them in ascending order of fitness value and 
        removes the last 2 chromosomes from population,the two worst chromosome having the maximum weight differences
        are removed"""
    def Add_Back_To_Population(self,fitA, randPopA, fitB, randPopB, fitness,Population):
        fitness.append(fitA)
        fitness.append(fitB)
        Population.append(randPopA)
        Population.append(randPopB)
        for i in range(0,len(fitness)):
            for j in range(0,len(fitness)-i-1):
                if fitness[j] > fitness[j+1]:
                    temp = fitness[j]
                    temp1 = Population[j]
                    fitness[j] = fitness[j+1]
                    Population[j] = Population[j+1]
                    fitness[j+1] = temp
                    Population[j+1] = temp1
        for i in range(0,2):
            fitness.pop()
            Population.pop()
        return fitness,Population
    """function to get input from the user"""
    def Get_Input(self):
        containers = int(input("Please enter the number of containers:  "))
        items = int(input("Please enter the number of items in containers:  "))
        option = int(input("Press 1 if you want items' weights to be as item weight/2 \nOr press 2 for weights as (item weight^2)/2: "))
        num = int(random.randrange(40,100))
        trials = int(input("Enter the number of trials: "))
        times = int(input("Enter the number of times you wish to perform mutation: "))
        return containers,items,option,num,trials,times
    
    """function to randomly create n chromosome and calculate their fitness"""
    def Apply_Initial_Steps(self):
        containers,items,option,num,trials,times = self.Get_Input()
        pop = self.Create_Populations(num,items, containers, option)
        fitness = self.All_Fitness(pop)
        return containers,items,option,num,fitness,pop,trials,times
    
    """prints the best overall fitness value and its chromosome"""
    def Print_Result(self,res):
        print("The best fitness value is", res[0])
        print("The best population is",res[1])
    
    """working of genetic algorithm"""
    def Genetic_Algorithm(self,trials,containers,items,fitness,pop,times,condition):
        #stores the best overall fitness value
        bestOVERALL = [float('inf'), None]
        #if crossover is to be applied
        if condition == "Crossover":
            while trials > 0:
                #selects to best chromosomes
                randPopA,randPopB,fitness = self.Ellitist_Wheel_Selection(fitness,pop) 
                randPopA, randPopB = self.Single_Point_Crossover(randPopA, randPopB)#crosover
                #applies mutation as per the mutation operator
                while times > 0:
                    randPopA, randPopB = self.Start_Mutation(randPopA, randPopB,items,containers)#mutation
                    times -= 1
                #calculates fitness values
                fitA = self.Calculate_Fitness(randPopA)
                fitB = self.Calculate_Fitness(randPopB)
                #adding the chromosomes back to population
                fitness,pop = self.Add_Back_To_Population(fitA, randPopA, fitB, randPopB, fitness,pop)
                #updating the result
                if fitA < bestOVERALL[0]:
                    bestOVERALL = (fitA, randPopA)
                if fitB < bestOVERALL[0]:
                    bestOVERALL = (fitB, randPopB)
                trials -= 1
#             self.Print_Result(bestOVERALL)
            return bestOVERALL[0]
        #if no crossover is to be applied
        else:
            while trials > 0:
                #selects to best chromosomes
                randPopA,randPopB,fitness = self.Ellitist_Wheel_Selection(fitness,pop) 
                #applies mutation as per the mutation operator
                while times > 0:
                    randPopA, randPopB = self.Start_Mutation(randPopA, randPopB,items,containers)#mutation
                    times -= 1
                #calculates fitness values
                fitA = self.Calculate_Fitness(randPopA)
                fitB = self.Calculate_Fitness(randPopB)
                #adding the chromosomes back to population
                fitness,pop = self.Add_Back_To_Population(fitA, randPopA, fitB, randPopB, fitness,pop)
                #updating the result
                if fitA < bestOVERALL[0]:
                    bestOVERALL = (fitA, randPopA)
                if fitB < bestOVERALL[0]:
                    bestOVERALL = (fitB, randPopB)
                trials -= 1
            return bestOVERALL[0]
#             self.Print_Result(bestOVERALL)



"""This fuction is used to run a given experiment for k trials"""
def Experimentation_Instance(pop_size,mutation_k,condition,instance):
    #if experiment for instance 1 is to be done
    if instance == 1:
        containers,items,option = 10,200,"A"
    #if experiment for instance 2 is to be done
    else:
        containers,items,option = 100,200,"B"
    all_fitness = []
    #generation values
    exp_trials = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    SCL = SmartCargoLoading() 
    #doing for 8 trials
    counter = 8
    while counter > 0:
        exp_fitness=[]
        for i in range(0,len(exp_trials)):
            pop = SCL.Create_Populations(pop_size,items,containers,option)
            fitness = SCL.All_Fitness(pop)
            res = SCL.Genetic_Algorithm(exp_trials[i],containers,items,fitness,pop,mutation_k,condition)
            exp_fitness.append(res)
        counter -= 1
        all_fitness.append(exp_fitness)
    return all_fitness


"""function to perform all 6 experiments for a given instance"""
def Result_Experimentation_Instance(instance):
    #creating a dictionary to store results for each expeiment
    all_results_instance = {}
    for i in range(1,7):
        key = "exp"+str(i)
        all_results_instance[key] = []
    #experiment1
    exp1_fitness = Experimentation_Instance(10,1,"Crossover",instance)
    all_results_instance["exp1"].append(exp1_fitness) 
    #experiment2
    exp2_fitness = Experimentation_Instance(100,1,"Crossover",instance)
    all_results_instance["exp2"].append(exp2_fitness) 
    #experiment3
    exp3_fitness = Experimentation_Instance(10,5,"Crossover",instance)
    all_results_instance["exp3"].append(exp3_fitness) 
    #experiment4
    exp4_fitness = Experimentation_Instance(100,5,"Crossover",instance)
    all_results_instance["exp4"].append(exp4_fitness) 
    #experiment5
    exp5_fitness = Experimentation_Instance(10,5,"None",instance)
    all_results_instance["exp5"].append(exp5_fitness) 
    #experiment6
    exp6_fitness = Experimentation_Instance(10,0,"Crossover",instance)
    all_results_instance["exp6"].append(exp6_fitness) 
    return all_results_instance


"""function to plot graphs for all trials of each experiment"""
def Plot_Graphs(result):
    for count in range(0,len(result)):
        t = "Graphs for Experiment" + str(count+1)
        print(t)
        key = "exp" + str(count+1)
        for i in range(0,len(result.get(key)[0])):
            exp_trials = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
            plt.plot(exp_trials, result.get(key)[0][i], color='red', marker='o')
            title = "Plot for trial " + str(i+1)
            plt.title(title, fontsize=14)
            plt.xlabel('Generation', fontsize=14)
            plt.ylabel('Fitness', fontsize=14)
            plt.grid(True)
            plt.show()

"""function to get the best fitness value for each trial of each experiment"""
def Get_Best_Fitness(result,):
    exp_trials = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    for count in range(0,len(result)):
        key = "exp" + str(count+1)
        print("Experiment ",count+1)
        for i in range(0,len(result.get(key)[0])):
            min_val = min(result.get(key)[0][i])
            min_index = result.get(key)[0][i].index(min_val)
            gen = exp_trials[min_index]
            print("Best Fitness for trial",i+1,"is: ",min_val,"for Generation",gen)
        print()
        
obj=SmartCargoLoading()
obj.Get_Input()
print("Plotting results:")
print("Instance 1 ")
resultsForInstance1 = Result_Experimentation_Instance(1)
Plot_Graphs(resultsForInstance1)
print("Instance 2")
resultsForInstance2 = Result_Experimentation_Instance(2)
Plot_Graphs(resultsForInstance2)
print("Best Fitness values:")
print("Instance 1")
Get_Best_Fitness(resultsForInstance1)
print("Instance 2")
Get_Best_Fitness(resultsForInstance2)

