'''
PRE-PREDICT-PROCESSING

This pre-processing step is designed to take a student's d2l data mid-term (ie n weeks into a semester) and create synthetic values to mimic the "end of term" data similar to what we used to train the model.
'''

import pandas as pd
import numpy as np
import math


# A function to add the engineered values - completion ratio, logins per course, average time spent per course login
def add_eng_values_pre_predict(X):
    
    
    # We want to create sythetic values for content_complete, quiz_completed, total_quiz_attmepts, discussion_post_read, and total_time_spent_in_content by multiplying each value by (total # of weeks in a term / current week in the term)
    X['content_completed'] = np.where(
    round(X['content_completed'] * (15 / X['week']), 0) >= X['content_required'],
    X['content_required'],
    round(X['content_completed'] * (15 / X['week']), 0)
)
    X['quiz_completed'] = round(X['quiz_completed']*(15/X['week']),0)
    X['total_quiz_attempts'] = round(X['total_quiz_attempts']*(15/X['week']),0)
    X['discussion_post_read'] = round(X['discussion_post_read']*(15/X['week']),0)
    X['number_of_assignment_submissions'] = round(X['number_of_assignment_submissions']*(15/X['week']),0)
    X['total_time_spent_in_content'] = round(X['total_time_spent_in_content']*(15/X['week']),0)
    
    X['completion_ratio'] = X['content_completed']/X['content_required']
    X['logins_per_course'] = X['number_of_logins_to_the_system']/((X['total_course_count']-X['course_count_by_term']) + X['course_count_by_term']*(X['week']/15))
    X['avg_time_per_login'] = X['total_time_spent_in_content']/X['logins_per_course']
    X['avg_time_by_completed_content'] = X['total_time_spent_in_content']/X['content_completed']
    X['quiz_attempts_per_quiz'] = X['total_quiz_attempts']/X['quiz_completed']
    X['number_of_logins_to_the_system'] = round(X['logins_per_course']*X['total_course_count'],0)
    
    X['completion_ratio'].fillna(0, inplace=True)
    X['avg_time_per_login'].fillna(0, inplace=True)
    X['course_count_by_term'].fillna(0, inplace=True)
    # Replace infinite values with NaN
    X['avg_time_by_completed_content'].replace([np.inf, -np.inf], np.nan, inplace=True)
    # Set values to zero where there is NaN (originally infinite)
    X['avg_time_by_completed_content'].fillna(0, inplace=True)
    
    # Replace infinite values with NaN
    X['quiz_attempts_per_quiz'].replace([np.inf, -np.inf], np.nan, inplace=True)
    # Set values to zero where there is NaN (originally infinite)
    X['quiz_attempts_per_quiz'].fillna(0, inplace=True)
    
    X.drop('week', axis=1, inplace=True)
    
    return X


# A function that changes format of 'term' value and imputes 'U' for missing gender values
def alter_term_gender_pre_predict(X_cat):
    
    # Alter format of 'term' value from 'DDDDS' to 'S'
    X_cat['term'] = X_cat['term'].str[-1]
    
    # Replace missing values in Gender column with 'U' for "undeclared"
    X_cat['gender'].fillna('U', inplace=True)
    
    return X_cat