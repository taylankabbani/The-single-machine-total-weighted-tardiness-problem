import pandas as pd
import random as rd

class FirstDescent():
    def __init__(self, Path, seed_num = 2012, iteration_num = 100):
        self.Path = Path
        self.iteration_num = iteration_num
        self.instance_dict = self.input_data()
        self.Initial_solution = self.get_InitialSolution(seed_num)
        self.Initial_objvalue = self.Objfun(self.Initial_solution)
        self.improvment_solution, self.improvment_objvalue = self.First_descent()

    def input_data(self):
        '''Takes the path of the excel file of the SMTWTP instances.
        Returns a dict of jobs number as Key and weight, processing time (hours) and due date (hours) as values.
        '''
        return pd.read_excel(self.Path,names = ['Job','weight',"processing_time", "due_date"],index_col=0).to_dict('index')

    def get_InitialSolution(self, seed_num, show=False):
        n_jobs = len(self.instance_dict) # Number of jobs
        # Producing a random schedule of jobs
        initial_solution = list(range(1, n_jobs+1))
        rd.seed(seed_num)
        rd.shuffle(initial_solution)
        if show == True:
            print("initial Random Solution: {}".format(initial_solution))
        return initial_solution

    def Objfun(self, solution, show = False):
        '''Takes a set of scheduled jobs, dict (input data)
        Return the objective function value of the solution
        '''
        dict = self.instance_dict
        t = 0   #starting time
        objfun_value = 0
        for job in solution:
            C_i = t + dict[job]["processing_time"]  # Completion time
            d_i = dict[job]["due_date"]   # due date of the job
            T_i = max(0, C_i - d_i)    #tardiness for the job
            W_i = dict[job]["weight"]  # job's weight

            objfun_value +=  W_i * T_i
            t = C_i
        if show == True:
            print("\n","#"*8, "The Objective function value for {} solution schedule is: {}".format(solution ,objfun_value),"#"*8)
        return objfun_value

    def SwapMove(self, li, show = False):
        '''Takes a list (solution)
        returns a new neighbor solution with randomly swapped elements
        '''
        li = li.copy()
        pos1 = rd.randint(0, len(li) - 1)  # picking two random jobs
        pos2 = rd.randint(0, len(li) - 1)
        if pos1 != pos2:
            li[pos1], li[pos2] = li[pos2], li[pos1]
        while pos1 == pos2:
            pos1 = rd.randint(0, len(li) - 1)  # picking two random jobs
            pos2 = rd.randint(0, len(li) - 1)
            if pos1 != pos2:
                li[pos1], li[pos2] = li[pos2], li[pos1]
                break
        if show == True:
            print("{} and {} are swapped, the current solution sequance is: {}".format(li[pos1], li[pos2], li))
        return li

    def First_descent(self):
        '''The implementation of a swap move (neighborhood operator) to improve the initial solution
        first improvement (first descent) strategy in applying the move.
        '''
        improvment_solution = self.Initial_solution
        improvment_objvalue = self.Initial_objvalue
        Terminate = 0  # Iterations without improvment solution found
        print("Initial solution: {}\n Objfun Value: {}".format(improvment_solution, improvment_objvalue))
        while Terminate < self.iteration_num :
            candidate_solution = self.SwapMove(improvment_solution)
            candidate_objvalue = self.Objfun(candidate_solution)
            if candidate_objvalue < improvment_objvalue:
                print('\n\n###', 'Improvment objvalue: {}, candidate objvalue: {} => Accepted'.format(
                    improvment_objvalue, candidate_objvalue))
                improvment_solution = candidate_solution
                improvment_objvalue = candidate_objvalue
                Terminate = 0
            else:
                print('#itr{}# Improvment objvalue: {}, candidate objvalue: {} => Not Accepted'.format(
                    Terminate, improvment_objvalue, candidate_objvalue))
                Terminate += 1
        print('*'*30,"Best Solution found: {}\n The value of the objective function: {}".format(improvment_solution,improvment_objvalue),'*'*30,sep ='\n\n')
        return improvment_solution, improvment_objvalue

instances_10 = FirstDescent(Path="Data_instances/Instance_10.xlsx", seed_num=2012, iteration_num=100)
# instances_20 = FirstDescent(Path="Data_instances/Instance_20.xlsx", seed_num=2012, iteration_num=100)
# instances_30 = FirstDescent(Path="Data_instances/Instance_30.xlsx", seed_num=2012, iteration_num=100)
