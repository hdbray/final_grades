import csv
from datetime import date

def letter_grade(y):
    if y.strip()=='':
        x=0
    else:
        x=float(y)
    if x>=97.5:
        return 'A+'
    elif x>=92.5:
        return 'A'
    elif x>=89.5:
        return 'A-'
    elif x>=87.5:
        return 'B+'
    elif x>=82.5:
        return 'B'
    elif x>=79.5:
        return 'B-'
    elif x>=77.5:
        return 'C+'
    elif x>=72.5:
        return 'C'
    elif x>=69.5:
        return 'C-'
    elif x>=59.5:
        return 'D'
    else:
        return 'F'


def print_grade_distribution(the_file,key_of_assessment,expanded=True, mastery=False): 

    # read the csv file

    file_list=[]

    with open(the_file) as openfile:
        reader=csv.reader(openfile) #, quotechar=None)
        for row in reader:
            file_list.append(row)

    # convert the list pulled from the csv to a dictionary
    grades_list_of_dicts=[]

    k=len(file_list)

    for i in range(k):
        grades_list_of_dicts.append({})
    
    headers=['Last Name']+file_list[0][1:]
    
    for i in range(k):
        for j in range(len(headers)):
            grades_list_of_dicts[i][headers[j]]=file_list[i][j]

    # start counting grades 
    countAps=0
    countAs=0
    countAms=0
    countBps=0
    countBs=0
    countBms=0
    countCps=0
    countCs=0
    countCms=0
    countDs=0
    countFs=0

    for k in range(1,len(grades_list_of_dicts)):
        score=grades_list_of_dicts[k][key_of_assessment]
        letter=letter_grade(score)

        if letter=='A+': 
            countAps+=1
        elif letter=='A': 
            countAs+=1
        elif letter=='A-':
            countAms+=1
        elif letter=='B+': 
            countBps+=1
        elif letter=='B': 
            countBs+=1
        elif letter=='B-':
            countBms+=1
        elif letter=='C+': 
            countCps+=1
        elif letter=='C': 
            countCs+=1
        elif letter=='C-':
            countCms+=1
        elif letter=='D':
            countDs+=1
        elif letter=='F':
            countFs+=1

    count0s=0

    if mastery==True:
        for k in range(1,len(grades_list_of_dicts)):
            score=grades_list_of_dicts[k][key_of_assessment]
            if float(score)==0:
                count0s = count0s+1



    print('letter grade distribution for '+grades_list_of_dicts[0][key_of_assessment])

    if expanded==True:
        print('A+s', countAps)
        print('As', countAs)
        print('A-s', countAms)
        print('B+s', countBps)
        print('Bs', countBs)
        print('B-s', countBms)
        print('C+s', countCps)
        print('Cs', countCs)
        print('C-s', countCms)
        print('Ds', countDs)
        print('Fs', countFs-count0s)

    else:
        countAs=countAms+countAps+countAs
        countBs=countBms+countBps+countBs
        countCs=countCms+countCps+countCs

        print('As', countAs)
        print('Bs', countBs)
        print('Cs', countCs)
        print('Ds', countDs)
        print('Fs', countFs-count0s)
    
    if mastery==True:
        print('zeros', count0s)
    

today=date.today()
date_str=today.strftime('%m_%d_%y')

bb_grades_file='bb_gc.csv'
todays_file=date_str+'_graded_'+bb_grades_file




## overall
#print('')
#print_grade_distribution(todays_file, 'Overall Course Grade Estimate [Total Pts: 100 Score] |3164280',False,False)
#
## unit 1 test
#print('')
#print_grade_distribution(todays_file, 'Unit 1 Test [Total Pts: 100 Score] |3164276',False,False)
#
## unit 2 test
#print('')
#print_grade_distribution(todays_file, 'Unit 2 Test [Total Pts: 100 Score] |3164292',False,False)
#
## mastery average
#print('')
#print_grade_distribution(todays_file, 'Mastery Problem Set Average [Total Pts: 100 Score] |3164274',False,True)
#
## worksheet average
#print('')
#print_grade_distribution(todays_file, 'Worksheet Average [Total Pts: 100 Score] |3164275',False,False)

## connect average
#print('')
#print_grade_distribution(todays_file, 'Connect Homework Average [Total Pts: 100 Score] |3164278',False,False)
#
# learnsmart average
print('')
print_grade_distribution(todays_file, 'LearnSmart Average [Total Pts: 100 Score] |3164277',False,False)
print('')
