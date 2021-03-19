
def write_email(student_name, course_grade, letter_grade, unit1_test, unit2_test,mastery_avg, connect_hw_avg,learnsmart_avg,worksheet_avg,mastery4,mastery5,num_connect_waivers_used,num_worksheet_waivers_used):

    unit_test_avg=.5*(unit1_test+unit2_test)

    improved_mastery=mastery_avg+(2-mastery4-mastery5)*20

    improved_course_grade=.45*unit_test_avg+.1*worksheet_avg+.1*connect_hw_avg+.05*learnsmart_avg+.3*improved_mastery

    course_grade=round(course_grade,2)
    unit_test_avg=round(unit_test_avg,2)
    mastery_avg=round(mastery_avg,2)
    connect_hw_avg=round(connect_hw_avg,2)
    learnsmart_avg=round(learnsmart_avg,2)
    worksheet_avg=round(worksheet_avg,2)
    improved_course_grade=round(improved_course_grade,2)

    email_opener='''Dear %s, 

This email is intended to give you an estimate of your course grade for Math 271. If your scores on future assessments resemble your scores for Units 1 and 2, then you would be on track to receive a course grade of %s, which corresponds to a letter grade of %s. 
    ''' % (student_name, course_grade, letter_grade)

    email_score_overview='''
This score is calculated using the following formula, as outlined in the syllabus, under the assumption that you receive the same average score on your remaining unit tests:

.45 x (unit test average = %s)
+ .1 x (worksheet average = %s)
+ .1 x (Connect  HW average = %s)
+ .05 x (LearnSmart average = %s)
+ .3 x (mastery problems average = %s)

    ''' % (unit_test_avg, worksheet_avg, connect_hw_avg, learnsmart_avg, mastery_avg)

    additional_calculation_remarks='''
These averages were calculated with all your waived assignments removed, as well as two additonal lowest Connect homework scores and two lowest LearnSmart scores, which were dropped for all students.  Also, LearnSmart 5.1 is only counted towards your grade if it benefits your course average, due to an error setting the assignment deadline, as discussed in class.  Lastly, any extra credit points were added to your overall worksheet total score which was then averaged out.  You are encouraged to double check that these averages are correct, and that the final calculation is correct, and report any concerns or discrepancies to me.  

The course grade estimate that will be entered into the midterm evaluations will be calculated after mastery problem set 4 version 3 and mastery problem set 5 version 2 are graded next Tuesday March 23. It will not include mastery problem set 6 version 1. 
    '''

    email_mastery=''

    if mastery4+mastery5<2:
        email_mastery='''
It is not too late to pass mastery problem set 4 and mastery problem set 5.  Note that the mastery problem sets are 30%% of your course grade, which is a significant portion of your overall grade.  If you pass both of these problem sets, then your course grade estimate improves to %s.  Please seek support in office hours with the mastery problem sets if you need it; the LAs are a fantastic resource and can talk through the past versions of mastery problem sets in detail to help you understand the concepts and how to complete the problems correctly. 
    ''' % (improved_course_grade)

    email_waivers='''
You have used %s waivers for the Connect homework assignments out of three available waivers, and you have used %s waivers for the worksheets out of the one available waiver. To apply any available waivers to future assignments, please contact me before the deadline by email to request and apply the waiver. The waiver policy was discussed in class and is written and available in the Syllabus page on Blackboard. 
    ''' % (num_connect_waivers_used, num_worksheet_waivers_used)

    email_signature='''
Please let me know if you have any questions about your grade calculation, or if you notice any discrepancies in your grade. Your unit 2 test feedback is available on Gradescope, and there are resources in Gradescope FAQs and support which go over how to access and view this feedback. The answer key to the unit 2 test is also posted on Blackboard in the same place as the test. The scores calculated above are also posted to Blackboard. 

Best,

Harry, on behalf of the 271 team
    '''

    email_body=email_opener+email_score_overview+additional_calculation_remarks+email_mastery+email_waivers+email_signature

    return email_body

