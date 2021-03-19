import csv
import subprocess
from datetime import date
import connect_grades_dict_file as cgd
import key_sets as ks
import waivers as ws
import email_script


### file names 

today=date.today()
date_str=today.strftime('%m_%d_%y')

bb_grades_file='bb_gc.csv'
gs_grades_file='gs.csv'
new_file=date_str+'_graded_'+bb_grades_file
email_file=date_str+'_email_script.csv'

### list names 

bb_grades_list=[]
gs_grades_list=[]
email_script_list=[['Email','Name','Body']]

# choose the last index you want to count 
# truncate file to this length
# if you don't want all assignments from bb gc to be incorporated
#end_index=26

# read file indices 

# for connect you have a pair (index, total points) for the assignment
# these are stored in the bb grade center
#connect_indices=[(23,120),(24,140),(25,70),(26,150)]
#learnsmart_indices=[19,20,21,22]
#
## in gs
#worksheet_indices=[12,16,20]
#mastery_indices=[4,8]
#
## in bb gc
#mastery3_index=17
#
#
### just for generating the email part 
#mastery1_index=4
#mastery2_index=8
#
#unit1_test_index=28
#unit2_test_index=unit1_test_index
#unit3_test_index=unit1_test_index
#unit4_test_index=unit1_test_index

# write file indices

target_overall_course_grade=7
target_letter_grade=8

target_mastery_avg_index=9
target_worksheet_avg_index=10
target_connect_hw_avg_index=11
target_learnsmart_avg_index=12

target_unit1_test_index=13
target_unit2_test_index=14
target_unit3_test_index=15
target_unit4_test_index=16


# this is how many assignments to drop

connect_default_num_drops=2
learnsmart_default_num_drops=2
worksheet_default_num_drops=0 
mastery_default_num_drops=0 

# maximum scores

learnsmart_max_score=100
worksheet_max_score=10
mastery_max_score=1

### functions

def calc_letter_grade(x):
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

def string_to_float(string):
    if string=='':
        return 0
    else:
        return float(string)

def remove_drops(list_name,num_drops):
    for i in range(num_drops):
        list_name.remove(min(list_name))
    return list_name

def num_connect_drops(name_pair):
    if name_pair in ws.set_with_one_connect_drop:
        return 1
    elif name_pair in ws.set_with_two_connect_drop:
        return 2
    elif name_pair in ws.set_with_three_connect_drop:
        return 3
    else:
        return 0

def num_worksheet_drops(name_pair):
    if name_pair in ws.set_with_worksheet_drop:
        return 1
    else:
        return 0

# this function takes a student dictionary of scores and the designated
# keys of interest and creates a list for the computed average, with a
# conditional for the case of connect

def key_set_to_list(student_entry_dict,key_set,is_connect=False):
    #student_entry_dict is a dictionary 
    #key_set is a set of keys that you want to use to form a list of grades
    #for computing their averages
    
    scores_list=[]
    if is_connect==True:
        for key in key_set:
            score=string_to_float(student_entry_dict[key])
            # the connect_grades_dict is stored in connect_grades_dict.py
            max_score=string_to_float(cgd.connect_grades_dict[key])
            scores_list.append((score,max_score))
    else:
        for key in key_set:
            scores_list.append(string_to_float(student_entry_dict[key]))
    return scores_list

    
# the calculate_connect_hw_scores function converts connect homework grades
# to a percentage and then drops the lowest grades and averages them out 

def calculate_connect_hw_scores(name_pair, connect_grade_pairs_list, num_drops=connect_default_num_drops):

    # name_pair is a pair (last_name, first_name) 
    # connect_grade_pairs_list is a list of pairs (student_score,
    # max_score) for each connect assignment

    percentages_list=[]

    # add extra drops for certain students
    # pull the drops sets from waivers.py

    num_drops+=num_connect_drops(name_pair)


    for pair in connect_grade_pairs_list: #index_pairs:
        score=string_to_float(pair[0])
        max_score=float(pair[1])
        percentages_list.append(100*score/max_score)

    with_drops=remove_drops(percentages_list,num_drops)

    connect_score=sum(with_drops)/len(with_drops)
    
    return connect_score


def calc_assignment_average(name_pair, student_scores, num_drops, max_points, worksheet=False, extra_credit=0):

    # add extra drops for certain students
    if worksheet==True:
        num_drops+=num_worksheet_drops(name_pair)
#        if name_pair in ws.set_with_worksheet_drop:
#            num_drops+=1

    # scores list with drops 
    new_student_scores=remove_drops(student_scores, num_drops)

    total_score=sum(new_student_scores)+extra_credit
    num_graded_assignments=len(new_student_scores)

    average=total_score/num_graded_assignments

    percentage=100*average/max_points

    return percentage

def calc_overall_score(unit1_test, unit2_test, unit3_test, unit4_test, connect_hw, connect_learnsmart, worksheet_avg, mastery_avg,without_tests=False ):

    option1=.1*(unit1_test+unit2_test+unit3_test)+.15*unit4_test+.1*connect_hw+.05*connect_learnsmart+.1*worksheet_avg+.3*mastery_avg 

    # in case you want to take the higher of two different grades later on
    option2=option1

    if without_tests==True:
        option1 = (.1*connect_hw+.05*connect_learnsmart+.1*worksheet_avg+.3*mastery_avg)/.6
        option2 = option1


    score=max(option1,option2)

    return score


### end functions
### start calculating the grades


### read the files and make lists

def calculate_grades(prep_email=True, check_names=True):

    with open(bb_grades_file) as open_file:
        reader=csv.reader(open_file, quotechar='"')
        for row in reader:
            bb_grades_list.append(row)   
    
    # for alphabetizing the gradescope list 
    
    pre_sorted_gs_grades_list=[]
    
    with open(gs_grades_file) as open_file:
        reader=csv.reader(open_file, quotechar='"')
        for row in reader:
            pre_sorted_gs_grades_list.append(row)
    
    ### alphabetize gradescope list 
    
    headers=pre_sorted_gs_grades_list[0]
    
    gs_grades_list.append(headers)
    
    names_for_sorting=pre_sorted_gs_grades_list[1:]
    
    names_for_sorting.sort(key=lambda a: a[1].lower())
    
    gs_grades_list.extend(names_for_sorting)
    
    
    ### now turn things into a dictionary
    
    grades_list_of_dicts=[]
    
    k=len(bb_grades_list)
    
    for i in range(k):
        grades_list_of_dicts.append({})
    
    bb_headers=['Last Name']+bb_grades_list[0][1:] 
    
    gs_headers=['GS First Name','GS Last Name']+gs_grades_list[0][2:] 
    
    for i in range(k):
        for j in range(len(bb_headers)):
            grades_list_of_dicts[i][bb_headers[j]]=bb_grades_list[i][j]
        for j in range(len(gs_headers)):
            grades_list_of_dicts[i][gs_headers[j]]=gs_grades_list[i][j]


#### now we are calculating the grades for real 

    
    for i in range(1,len(grades_list_of_dicts)):
        student_row_dict=grades_list_of_dicts[i]
    
        first_name=student_row_dict['First Name']
        last_name=student_row_dict['Last Name']
        name_pair=(last_name,first_name)
    
        # for writing the email
        student_name=first_name+' '+last_name
        email=student_row_dict['Username']+'@gmu.edu'
        mastery4=string_to_float(student_row_dict['Mastery Problem Set 4: Addition and Subtraction (version 2 of 3)'])
        mastery5=string_to_float(student_row_dict['Mastery Problem Set 5: Multiplication and Division of Integers (version 1 of 3)'])
        num_connect_waivers_used=num_connect_drops(name_pair)
        num_worksheet_waivers_used=num_worksheet_drops(name_pair)
    
        # extra credit
    
        extra_credit_grades_list=key_set_to_list(student_row_dict,ks.extra_credit_keys)
        extra_credit_total=sum(i for i in extra_credit_grades_list)
    
        # connect grades
    
        connect_grade_pairs_list=key_set_to_list(student_row_dict,ks.connect_hw_keys,True)
        connect_grade_pairs_list_wo_5_1=key_set_to_list(student_row_dict,ks.connect_hw_keys_without_5_1,True)
    
        connect_hw_opt1 = calculate_connect_hw_scores(name_pair, connect_grade_pairs_list, num_drops=connect_default_num_drops)
    
        connect_hw_opt2 = calculate_connect_hw_scores(name_pair, connect_grade_pairs_list_wo_5_1, num_drops=connect_default_num_drops)
    
        connect_hw_avg=max(connect_hw_opt1,connect_hw_opt2)
    
        # worksheet grades
        # this is where extra credit gets incorporated
    
        worksheet_grades_list=key_set_to_list(student_row_dict,ks.worksheet_keys)
        
        worksheet_avg=calc_assignment_average(name_pair, worksheet_grades_list, worksheet_default_num_drops, worksheet_max_score, True, extra_credit_total)
    
    
        # learnsmart grades
    
        learnsmart_grades_list=key_set_to_list(student_row_dict,ks.learnsmart_keys)
        
        learnsmart_avg=calc_assignment_average(name_pair, learnsmart_grades_list, learnsmart_default_num_drops, learnsmart_max_score, False)
    
    
        # mastery grades
    
        mastery_grades_list=key_set_to_list(student_row_dict,ks.mastery_keys)
        
        mastery_avg=calc_assignment_average(name_pair, mastery_grades_list, mastery_default_num_drops, mastery_max_score, False)
    
    
        # test grades
    
        unit1_test=string_to_float(student_row_dict[ks.unit1_test_key])
        unit2_test=string_to_float(student_row_dict[ks.unit2_test_key])
    #    unit3_test=string_to_float(student_row_dict[ks.unit3_test_key])
    #    unit4_test=string_to_float(student_row_dict[ks.unit4_test_key])
    #    unit2_test=unit1_test
    #    unit3_test=unit1_test
    #    unit4_test=unit1_test
        unit3_test=.5*(unit1_test+unit2_test)
        unit4_test=.5*(unit1_test+unit2_test)
    #    unit2_test=student_row_dict[ks.unit2_test_key]
    #    unit3_test=student_row_dict[ks.unit3_test_key]
    #    unit4_test=student_row_dict[ks.unit4_test_key]
    
    
        # overall course grade and letter grade
    
        overall_score=calc_overall_score(unit1_test, unit2_test, unit3_test, unit4_test, connect_hw_avg, learnsmart_avg, worksheet_avg, mastery_avg)
    
        letter_grade=calc_letter_grade(overall_score)
    
        # add everything to the bb_grades_list  
    
        bb_grades_list[i][target_connect_hw_avg_index]=connect_hw_avg
        bb_grades_list[i][target_learnsmart_avg_index]=learnsmart_avg
        bb_grades_list[i][target_mastery_avg_index]=mastery_avg
        bb_grades_list[i][target_worksheet_avg_index]=worksheet_avg
    
    
        bb_grades_list[i][target_unit1_test_index]=unit1_test
        bb_grades_list[i][target_unit2_test_index]=unit2_test
    #    bb_grades_list[i][target_unit3_test_index]=unit3_test
    #    bb_grades_list[i][target_unit4_test_index]=unit4_test
    
        bb_grades_list[i][target_overall_course_grade]=overall_score
        bb_grades_list[i][target_letter_grade]=letter_grade
    
    
        ##### write email
    
    
        
        if prep_email==True:
            emailbody=email_script.write_email(student_name, overall_score, letter_grade, unit1_test, unit2_test,mastery_avg, connect_hw_avg,learnsmart_avg,worksheet_avg,mastery4,mastery5,num_connect_waivers_used,num_worksheet_waivers_used)
        
            email_script_list.append([])
            email_script_list[i].append(email)
            email_script_list[i].append(student_name)
            email_script_list[i].append(emailbody)
    
    # currently bb_grades_list has everything
    # cut the tails of bb_grades_list so that you don't accidentally overwrite
    # something that you don't intend to when uploading
    
    truncated_bb_grades_list=[]
    
    for i in range(len(bb_grades_list)):
        truncated_bb_grades_list.append(bb_grades_list[i][:17])
    
    # now write the updated bb_grades_list to the new_file csv 
    
    with open(new_file, 'w+') as write_file:
        write=csv.writer(write_file)
        write.writerows(truncated_bb_grades_list)
    
    # open the new csv with your default program (mine is excel). note that it
    # will not update so you have to close the old one before running the
    # script
    
    subprocess.run(['open', new_file], check=True)
    
    if prep_email==True:
        with open(email_file, 'w+') as write_file:
            write=csv.writer(write_file)
            write.writerows(email_script_list)
        
        subprocess.run(['open', email_file], check=True)
    
    ### check that the names match up in the two different files 
    
    if check_names==True:
        print('''

Checking whether the names match up in the Blackboard and Gradescope files.
Any mismatches will be printed below.

    ''')
        for student_entry_dict in grades_list_of_dicts:
            if student_entry_dict['Last Name']!=student_entry_dict['GS Last Name']:
                print('BB: '+student_entry_dict['Last Name']+' ---  GS: '+student_entry_dict['GS Last Name']) 

        print('')
        print('')
    

#calculate_grades()
# write the email but don't check names
calculate_grades(True,False)
# just calculate grades, without writing the email or checking names
#calculate_grades(False,False)




