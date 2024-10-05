import numpy as np
import pandas as pd
import re
import random

# assing values
toa_first = 1
toa_second = 1
toa = 1
rho = 0.5 #

c1 = np.matrix([[77,6,62,7],[39,72,95,59],[34,82,27,6],[75,42,27,77]]) #

# check what is the bound
def CkeckCummProbBound(number,cummProb):
    if number < cummProb[0]:
        return cummProb[0]
    
    for i in range(len(cummProb)-1):
        if cummProb[i] <= number < cummProb[i+1]:
            return cummProb[i+1]
           
    return cummProb[-1]

# method for generate table 3.1 of the provided document
def Table3_1(c1,toa):
    df = pd.DataFrame(columns=['path','first_row',"eta",'toa','toa x eta'])

    for i in zip(c1[0]):
        iteration = len(np.array(i).flatten())
        for k in range(iteration):
            path = f"0 -> {k}"
            first_metrix_row = np.array(i).flatten()[k]
            eta = 1/np.array(i).flatten()[k]
            toaEta = toa * eta

            df.loc[len(df)] = {'path':path,'first_row':first_metrix_row,'eta':eta,'toa':toa,'toa x eta':toaEta}
                   
    return df

def Table3_2(df):
    df_trans_prob = pd.DataFrame(columns=['path','probability','cumm. prob.'])

    cummProb = []
    cummProbPath = []
    probability = []
    total_eta_values = []
    value_path = []

    toa = []
    eta = []

    for i in df.iloc[:,-5]:
        value_path.append(i)

    for i in df.iloc[:,-2]:
        toa.append(i)

    for i in df.iloc[:,-3]:
        eta.append(i)

    sum_toa_eta = 0

    for i in range(len(toa)):
        sum_toa_eta = sum_toa_eta + ((toa[i]) * (eta[i]))

    totalOfAllEtaValues = sum(total_eta_values)

    for i in range(len(toa)):
        prob = ((toa[i])*eta[i])/(sum_toa_eta)
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
        df_eta_list = []

        uniquPathNames = list(set(path_list_name))
        uniquPathValues = list(set(path_list))

        for i in df.iloc[:,-3]:
            df_eta_list.append(i)

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

            new_toa = (1-rhoValue)*(df.loc[index, 'toa'])

            for i in values:
                new_toa = new_toa + df_eta_list[i]

            df['toa'] = df['toa'].astype(float)

            df.loc[index,'toa'] = new_toa

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
    # print("c2 mettrix: ",c2)
    print()

    x = Table3_1(c1,toa)
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

    # deletedElementOfC2 = c2[pathNameList[0],pathNameList[1]]
    # c2 = np.delete(c2,pathNameList[0],axis=0)
    # c2 = np.delete(c2,pathNameList[1],axis=1)
    
    RemovedValuesOfMetrixes.append(f"({deletedElementOfC1})")
    round = round + 1

print()
print(f"\U0001F7E5 {round} Round ----------------------->>>>>>>>>>>")
print(f"c1: {c1}")

print("------------------------------------------------------------------------------------")
RemovedValuesOfMetrixes.append(f"({c1.item()})")
RemoveElementIntList = int_list = [eval(expr) for expr in RemovedValuesOfMetrixes]
output = f"\U0001F7E2 optimum value = {' + '.join(RemovedValuesOfMetrixes)} = {sum(RemoveElementIntList)}"
print(output)
print("---------------End----------------")