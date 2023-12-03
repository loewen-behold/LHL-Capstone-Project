'''
DATA-PROCESSING

This pre-processing recieves a .xlsx file and returns a cleaned file.
'''

import pandas as pd
import numpy as np


# A function to add the engineered values - completion ratio, logins per course, average time spent per course login
def add_eng_values(X):
    
    X['completion_ratio'] = X['content_completed']/X['content_required']
    X['logins_per_course'] = X['number_of_logins_to_the_system']/X['total_course_count']
    X['avg_time_per_login'] = X['total_time_spent_in_content']/X['logins_per_course']
    X['avg_time_by_completed_content'] = X['total_time_spent_in_content']/X['content_completed']
    
    X['completion_ratio'].fillna(0, inplace=True)
    X['avg_time_per_login'].fillna(0, inplace=True)
    X['course_count_by_term'].fillna(0, inplace=True)
    # Replace infinite values with NaN
    X['avg_time_by_completed_content'].replace([np.inf, -np.inf], np.nan, inplace=True)

    # Set values to zero where there is NaN (originally infinite)
    X['avg_time_by_completed_content'].fillna(0, inplace=True)
    
    return X


# A function that changes format of 'term' value and imputes 'U' for missing gender values
def alter_term_gender(X_cat):
    
    # Alter format of 'term' value from 'DDDDS' to 'S'
    X_cat['term'] = X_cat['term'].str[-1]
    
    # Replace missing values in Gender column with 'U' for "undeclared"
    X_cat['gender'].fillna('U', inplace=True)
    
    return X_cat


# Function receives three dataframes from the sourse xlsx called "d2l", "df_demo", and "df_grades"
def df_construct(df_d2l, df_demo, df_grades):
    
    # Drop duplicates based on the specified columns, keeping the first occurrence (which has the largest 'content_completed')
    df_d2l.sort_values(by='content_completed', ascending=False, inplace=True)
    df_d2l.drop_duplicates(subset=['pseudo_id', 'pseudo_course', 'term'], keep='first', inplace=True)
    
    # Drop all date columns
    df_d2l.drop(columns=['last_discussion_post_date', 'last_assignment_submission_date', 'last_system_login',
                         'last_quiz_attempt_date', 'last_visited_date'], axis=1, inplace=True)
    
    # appending the "grade_value" column into the df_d2l dataframe (if there is no grade, a zero is input)
    df_d2l['grade_value'] = df_d2l.apply(lambda row: df_grades[
        (df_grades['pseudo_student_id'] == row['pseudo_id']) & 
        (df_grades['pseudo_course_name'] == row['pseudo_course']) &
        (df_grades['term'] == row['term'])
    ]['grade_value'].values[0] if not df_grades[
        (df_grades['pseudo_student_id'] == row['pseudo_id']) & 
        (df_grades['pseudo_course_name'] == row['pseudo_course']) &
        (df_grades['term'] == row['term'])
    ].empty else 0, axis=1)
    
    # append 'gender', 'imm_status', 'age' onto dataframe - joined on student id
    merged_df = pd.merge(df_d2l, df_demo[['pseudo_student_id', 'gender', 'imm_status', 'age']], 
                         left_on='pseudo_id', right_on='pseudo_student_id', how='left')
    merged_df.drop('pseudo_student_id', axis=1, inplace=True)
    
    # Append the total course counts for each student
    course_counts_df = df_grades.groupby('pseudo_student_id')['pseudo_course_name'].count().reset_index()
    course_counts_df.columns = ['pseudo_student_id', 'total_course_count']

    merged_df = pd.merge(merged_df, course_counts_df, left_on='pseudo_id', right_on='pseudo_student_id', how='left')
    merged_df.drop('pseudo_student_id', axis=1, inplace=True)
    
    # Append the total course counts for each student by term
    course_counts_by_term_df = df_grades.groupby(['pseudo_student_id','term'])['pseudo_course_name'].count().reset_index()
    course_counts_by_term_df.columns = ['pseudo_student_id', 'term', 'course_count_by_term']

    merged_df = pd.merge(merged_df, course_counts_by_term_df, left_on=['pseudo_id','term'], right_on=['pseudo_student_id', 'term'], how='left')
    merged_df.drop('pseudo_student_id', axis=1, inplace=True)
    
    # drop student id from df
    merged_df.drop('pseudo_id', axis=1, inplace=True)
    
    # Add engineered values
    merged_df = add_eng_values(merged_df)
    
    # Alter categorical columns as necessary
    merged_df = alter_term_gender(merged_df)
    
    # Apply the function to create the 'at_risk' column that classifies any students with a 1.0 or below as "at-risk"
    merged_df['at_risk'] = merged_df['grade_value'].apply(lambda grade: 1 if grade < 1.0 else 0)
    
    # drop grade_value from df
    merged_df.drop('grade_value', axis=1, inplace=True)
    
    return merged_df