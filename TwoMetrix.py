import numpy as np
import pandas as pd
import re
import random

sizeOfTheMatrix = int(input("Enter the size of the matrix: "))
weight = float(input("Enter the weight: "))
rho = float(input("Enter the rho: "))

weight1 = weight
weight2 = weight

c1 = np.matrix(np.random.randint(1, 100, size=(sizeOfTheMatrix, sizeOfTheMatrix)))
c2 = np.matrix(np.random.randint(1, 100, size=(sizeOfTheMatrix, sizeOfTheMatrix)))

# assing values
# weight1 = 0.5 #
# weight2 = 0.5 #
toa_first = 1
toa_second = 1
# rho = 0.5 #

# c1 = np.matrix([[77,6,62,7],[39,72,95,59],[34,82,27,6],[75,42,27,77]]) #
# c2 = np.matrix([[36,55,1,95],[8,23,78,20],[42,3,34,20],[14,55,78,68]]) #

# check what is the bound
def CkeckCummProbBound(number,cummProb):
    if number < cummProb[0]:
        return cummProb[0]
    
    for i in range(len(cummProb)-1):
        if cummProb[i] <= number < cummProb[i+1]:
            return cummProb[i+1]
           
    return cummProb[-1]

# method for generate table 3.1 of the provided document
def Table3_1(c1,c2,toa1,toa2):
    df = pd.DataFrame(columns=['path','first_row','second_row','toa_first','toa_second','eta_first','eta_second','total_eta'])

    for i,j in zip(c1[0],c2[0]):
        iteration = len(np.array(i).flatten())
        for k in range(iteration):
            path = f"0 -> {k}"
            first_metrix_row = np.array(i).flatten()[k]
            second_metrix_row = np.array(j).flatten()[k]
            eta_first = 1/np.array(i).flatten()[k]
            eta_second = 1/np.array(j).flatten()[k]
            total_eta = eta_first + eta_second

            df.loc[len(df)] = {'path':path,'first_row':first_metrix_row,'second_row':second_metrix_row,
                            'toa_first':toa1,'toa_second':toa2,'eta_first':eta_first,'eta_second':eta_second,'total_eta':total_eta}
                   
    return df

def Table3_2(df):
    df_trans_prob = pd.DataFrame(columns=['path','probability','cumm. prob.'])

    cummProb = []
    cummProbPath = []
    probability = []
    total_eta_values = []
    value_path = []

    toa_first = []
    toa_second = []
    eta_first = []
    eta_second = []

    # store in total of eta value of each metrixes first row
    for i in df.iloc[:,-1]:
        total_eta_values.append(i)
    
    for i in df.iloc[:,-8]:
        value_path.append(i)

    for i in df.iloc[:,-5]:
        toa_first.append(i)

    for i in df.iloc[:,-4]:
        toa_second.append(i)

    for i in df.iloc[:,-3]:
        eta_first.append(i)

    for i in df.iloc[:,-2]:
        eta_second.append(i)

    sum_toa_eta = 0

    for i in range(len(toa_first)):
        sum_toa_eta = sum_toa_eta + ((toa_first[i] + toa_second[i]) * (total_eta_values[i]))

    #print("sum eta and toa: ",sum_toa_eta)

    totalOfAllEtaValues = sum(total_eta_values)

    for i in range(len(toa_first)):
        prob = ((toa_first[i] + toa_second[i])*total_eta_values[i])/(sum_toa_eta)
        probability.append(prob)

    for i in range(len(probability)):
        if (i == 0):
            cummProb.append(probability[i])
            cummProbPath.append(value_path[i])
            df_trans_prob.loc[len(df_trans_prob)] = {"path": value_path[i],'probability':probability[i],'cumm. prob.':probability[i]}
        else:
            cummProb.append(cummProb[i-1] + probability[i])
            cummProbPath.append(value_path[i])
            df_trans_prob.loc[len(df_trans_prob)] = {"path":value_path[i],'probability':probability[i],'cumm. prob.': cummProb[i-1] + probability[i]}

    return cummProb,cummProbPath,df_trans_prob

def Table3_4(cummProb,cummProbPath,rhoValue,df):
    random_numbers = [random.random() for _ in range(len(cummProb))]
    # print()
    print("Random Numbers: ", random_numbers)
    # print()
    #print("CummProb: ", cummProb)

    path_list = []
    path_list_name = []

    for i in range(len(random_numbers)):
        nearet_number = CkeckCummProbBound(random_numbers[i],cummProb)

        for j in range(len(cummProb)):
            if (cummProb[j] == nearet_number):
                path_list_name.append(cummProbPath[j])

        path_list.append(nearet_number)

    # print()
    # print("Path List Name: ",path_list_name)
    # print("Path List: ",path_list)
    # print("--------------------------------------")

    isPathsEqual = all(num == path_list[0] for num in path_list)

    if isPathsEqual == True:
        uniquPathValues = list(set(path_list))
        #path = df_trans_prob.loc[df_trans_prob['cumm. prob.'] == uniquPathValues[0], 'path'].values[0]
        print()
        #print(df)
        # print()
        # print("Random Numbers: ", random_numbers)
        # print()
        # cummProb,cummProbPath,df_trans_prob = Table3_2(df)
        # print(df_trans_prob)
        # print()
        print("Final path: ",path_list_name[0])
        return f"Final path: {path_list_name[0]}"
        
    else:
        df_eta_first_list = []
        df_eta_second_list = []
        uniquPathNames = list(set(path_list_name))
        uniquPathValues = list(set(path_list))

        for i in df.iloc[:,-3]:
            df_eta_first_list.append(i)

        for j in df.iloc[:,-2]:
            df_eta_second_list.append(j)

        z_indices = {value: [] for value in uniquPathNames}

        for index, value in enumerate(path_list_name):
            z_indices[value].append(index)

        # print("Unique values in y:", path_list_name)
        # print("Indices of x according to z values:", z_indices)

        # Remove rows from the dataframe
        for i in df['path']:
            if i not in uniquPathNames:
                #print(i,"not in df")
                index = df.loc[df['path'] == i].index
                df = df.drop(index=index)
            
        # update toa values
        for keys,values in z_indices.items():

            index = df.loc[df['path'] == keys].index

            new_toe_1 = (1-rhoValue)*weight1*(df.loc[index, 'toa_first'])
            new_toe_2 = (1-rhoValue)*weight2*(df.loc[index, 'toa_second'])

            for i in values:
                new_toe_1 = new_toe_1 + df_eta_first_list[i]
                new_toe_2 = new_toe_2 + df_eta_second_list[i]

            df['toa_first'] = df['toa_first'].astype(float)
            df['toa_second'] = df['toa_second'].astype(float)


            df.loc[index,'toa_first'] = new_toe_1
            df.loc[index,'toa_second'] = new_toe_2

        print(df)
        cummProb,cummProbPath,df_trans_prob = Table3_2(df)
        print(df_trans_prob)
        print()
        print("-------------------------------end of a round-----------------------------------------------------")
        print()
        return Table3_4(cummProb,cummProbPath,rho,df)


RemovedValuesOfMetrixes = []

round  = 1
while (c1.shape != (1,1)):

    print()
    print(f"\U0001F7E5 {round} Round ----------------------->>>>>>>>>>>")
    print()

    print("c1 matrix: ",c1)
    print("c2 mettrix: ",c2)
    print()

    x = Table3_1(c1,c2,toa_first,toa_second)
    print(x)
    cummProb,cumprobPath,df_trans_prob =  Table3_2(x)
    # print(cummProb)
    # print(cumprobPath)
    print(df_trans_prob)
    pathName= Table3_4(cummProb,cumprobPath,rho,x)
    pathNameValues = re.findall(r'\d+', pathName)
    pathNameList = list(map(int, pathNameValues))

    # Delete each row and column
    deletedElementOfC1 = c1[pathNameList[0],pathNameList[1]]
    c1 = np.delete(c1,pathNameList[0],axis=0)
    c1 = np.delete(c1,pathNameList[1],axis=1)

    deletedElementOfC2 = c2[pathNameList[0],pathNameList[1]]
    c2 = np.delete(c2,pathNameList[0],axis=0)
    c2 = np.delete(c2,pathNameList[1],axis=1)
    
    RemovedValuesOfMetrixes.append(f"({deletedElementOfC1}+{deletedElementOfC2})")
    round = round + 1

print()
print(f"\U0001F7E5 {round} Round ----------------------->>>>>>>>>>>")
print(f"c1: {c1}")
print(f"c2: {c2}")

print("------------------------------------------------------------------------------------")
RemovedValuesOfMetrixes.append(f"({c1.item()}+{c2.item()})")
# print(f"\U0001F7E2 c1: {c1}")
# print(f"\U0001F7E2 c2: {c2}")
RemoveElementIntList = int_list = [eval(expr) for expr in RemovedValuesOfMetrixes]
output = f"\U0001F7E2 optimum value = {' + '.join(RemovedValuesOfMetrixes)} = {sum(RemoveElementIntList)}"
print(output)
print("---------------End----------------")
