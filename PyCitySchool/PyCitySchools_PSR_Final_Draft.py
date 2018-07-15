
# coding: utf-8

# ## PyCity School Analysis
# 
# 

# ### Analysis
# 
# * __*39,170 students*__ completed both the Math and Reading assesments within the District.
# * The passing rate in Reading was 85.5%; for Math it is 74.9%.  This suggests that students are __*more proficinet in Reading than Math*__.
# * __*Overall Reading and Math peformance is greater in charters schools than in district schools*__.  The overall passing rate in charters schools (90.6%) exceeds district schools (53.7%) by 36.9 percentage points.
# * __*Overall Reading and Math peformance is greater in schools with less than 2,000 students*__.  The overall passing rate in schools with less than 2,000 students exceeds 90%, while the overall passing rate for schools with more than 2,000 students is 56%.
# * __*Overall Reading and Math peformance is greater in schools that spend less than 615 dollars per student*__.  The overall passing rate in schools that spend less than 615 dollars per students exceeds 90%, while the overall passing rate for schools that spend more than 615 dollars per student is equal to (or less than) 60.3%.

# ### District Summary

# In[1]:


#Required Dependencies

import pandas as pd
import numpy as np
import os


# In[2]:


#Files to load

school_data_to_load = "schools_complete.csv"
student_data_to_load = "students_complete.csv"


# In[3]:


#Read school and student data file.  Store into Pandas data frames

school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)


# In[4]:


#print the first few results from "school_data"

school_data.head()


# In[5]:


#print the first few results from "student_data"

student_data.head()


# In[6]:


#Left join merge "school_data" and "student_data" tables

school_data_complete = pd.merge(school_data, student_data, on="school_name", how="left")
school_data_complete.head()


# In[7]:


#Identify incomplete rows by using count and comparing values

school_data_complete.count()


# In[8]:


#Verify the data types on the data frame

school_data_complete.dtypes


# ### District Summary

# In[9]:


#List school names

school_names = school_data_complete['school_name'].unique()
school_names


# In[10]:


#Number of schools in district

school_count = len(school_names)
school_count


# In[11]:


#Number of students in district

student_count = school_data_complete['Student ID'].count()
student_count


# In[12]:


#Total district budget

total_budget = school_data_complete["budget"].unique().sum()
total_budget


# In[13]:


#Average math score

average_math = school_data_complete["math_score"].mean()
average_math


# In[14]:


#Average reading score

average_reading = school_data_complete["reading_score"].mean()
average_reading


# In[15]:


#Percentage of students with a passing math scores of 70 or greater.

raw_math_data = school_data_complete["math_score"]
percent_passing_math = (raw_math_data >= 70).sum() / 39170
percent_passing_math


# In[16]:


#Percentage of students with a passing Reading scores of 70 or greater.

raw_reading_data = school_data_complete["reading_score"]
percent_passing_reading =(raw_reading_data >= 70).sum() / 39170 
percent_passing_reading


# In[17]:


#Percentage Overall Passing Rate

overall_passing_rate_percent = (average_math + average_reading) / 2
overall_passing_rate_percent


# In[18]:


# district dataframe from dictionary

district_summary = pd.DataFrame({
    
    "Total Schools": [school_count],
    "Total Students": [student_count],
    "Total Budget": [total_budget],
    "Average Reading Score": [average_reading],
    "Average Math Score": [average_math],
    "% Passing Reading":[percent_passing_reading],
    "% Passing Math": [percent_passing_math],
    "Overall Passing Rate": [overall_passing_rate_percent]

})

#store as different df to change order
#dist_sum = district_summary[["Total Schools", 
#                          "Total Students", 
#                         "Total Budget", 
#                           "Average Reading Score", 
#                           "Average Math Score", 
#                           '% Passing Reading', 
#                           '% Passing Math', 
#                           'Overall Passing Rate']]

#format cells
district_summary.style.format({"Total Budget": "${:,.2f}", 
                       "Average Reading Score": "{:.1f}", 
                       "Average Math Score": "{:.1f}", 
                       "% Passing Math": "{:.1%}", 
                       "% Passing Reading": "{:.1%}", 
                       "Overall Passing Rate": "{:.1f}"})


# ### School Summary

# In[19]:


#Group by school

group_by_school = school_data_complete.set_index('school_name').groupby(['school_name'])


# In[20]:


#Type of school

school_type = school_data_complete.set_index('type')['school_name'].drop_duplicates()


# In[21]:


#Total students by school

total_students_by_school = group_by_school['student_name'].count()
total_students_by_school


# In[22]:


#school type

district_charter = school_data_complete.drop_duplicates(['school_name'], keep="first").set_index('school_name')['type']
district_charter


# In[23]:


#school budget

school_budget = school_data_complete.set_index('school_name')['budget'].drop_duplicates()
school_budget


# In[24]:


#Spending per student

spending_per_student = school_budget/total_students_by_school
spending_per_student


# In[25]:


#Average math scores by school

average_math = group_by_school['math_score'].mean()
average_math


# In[26]:


#Average scores by school

average_reading = group_by_school['reading_score'].mean()
average_reading


# In[27]:


#Percent passing scores by school

pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('school_name')['Student ID'].count()/total_students_by_school 
pass_math


# In[28]:


#Percent passing scores by school

pass_reading = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('school_name')['Student ID'].count()/total_students_by_school 
pass_reading


# In[29]:


#Percent passing scores by school

overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('school_name')['Student ID'].count()/total_students_by_school 
overall


# In[30]:


#Convert school summary calculations into data frames

school_type_df = pd.DataFrame(school_type)

district_charter_df = pd.DataFrame(district_charter)

total_students_by_school_df = pd.DataFrame(total_students_by_school)

school_budget_df = pd.DataFrame(school_budget)

spending_per_student_df = pd.DataFrame(spending_per_student)

average_math_df = pd.DataFrame(average_math)

average_reading_df = pd.DataFrame(average_reading)

pass_math_df = pd.DataFrame(pass_math)

pass_reading_df = pd.DataFrame(pass_reading)

overall_df = pd.DataFrame(overall)


# In[31]:


#label - per student spending
spending_per_student_df = spending_per_student_df.rename(columns={spending_per_student_df.columns[0]: 'per student spending'})
spending_per_student_df.head()


# In[32]:


#label - % passing math
pass_math_df = pass_math_df.rename(columns={pass_math_df.columns[0]: '% passing math'})
pass_math_df.head()


# In[33]:


#label - % passing reading
pass_reading_df = pass_reading_df.rename(columns={pass_reading_df.columns[0]: '% passing reading'})
pass_reading_df.head()


# In[34]:


#label - overall passing
overall_df = overall_df.rename(columns={overall_df.columns[0]: 'overall passing rate'})
overall_df.head()


# In[35]:


#Combined data frames to a single object

summary_df =  (school_type_df,
              district_charter_df,
              total_students_by_school_df,
              school_budget_df,
              spending_per_student_df,
              average_math_df,
              average_reading_df,
              pass_math_df,
              pass_reading_df,
              overall_df)


# In[36]:


#Merged "summary_df" using: reduce, lambda, and left join

from functools import reduce;

summary_df_merged = reduce(lambda left,right: pd.merge(left,right,on=['school_name'], how='left'), summary_df)


#Renamed columns

summary_df_merged.rename(columns={
    summary_df_merged.columns[0]: 'school name',
    summary_df_merged.columns[2]: 'number of students',
    summary_df_merged.columns[4]: 'per student spending',
    summary_df_merged.columns[5]: 'math score',
    summary_df_merged.columns[6]: 'reading score',
    summary_df_merged.columns[7]: '% passing rate math',
    summary_df_merged.columns[8]: '% passing rate reading',
    summary_df_merged.columns[9]: '% overall passing rate'
}, inplace=True)


#Format columns (using map)

summary_df_merged['budget'] = summary_df_merged['budget'].map('${:,.2f}'.format)
summary_df_merged['per student spending'] = summary_df_merged['per student spending'].map('${:,.2f}'.format)
summary_df_merged['math score'] = summary_df_merged['math score'].map('{:.1f}'.format)
summary_df_merged['reading score'] = summary_df_merged['reading score'].map('{:.1f}'.format)
summary_df_merged['% passing rate math'] = summary_df_merged['% passing rate math'].map('{:.1%}'.format)
summary_df_merged['% passing rate reading'] = summary_df_merged['% passing rate reading'].map('{:.1%}'.format)
summary_df_merged['% overall passing rate'] = summary_df_merged['% overall passing rate'].map('{:.1%}'.format)


#Print summary table
summary_df_merged.head (20)


# ### Top five performing schools by overall passing rate

# In[37]:


# School summary table sorted by overall passing rate (top schools)

top_five_overall_passing_df = summary_df_merged.sort_values('% overall passing rate', ascending=False).reset_index(drop=True)

top_five_overall_passing_df.head (5)


# ### Lowest five performing schools by overall passing rate

# In[38]:


# School summary table sorted by overall passing rate (lowest schools)

bottom_five_overall_passing_df = top_five_overall_passing_df.tail().reset_index(drop=True)

bottom_five_overall_passing_df.head (5)


# ### Math scores by grade

# In[39]:


#creates grade level average math scores for each school 
ninth_math = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')["math_score"].mean()
tenth_math = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')["math_score"].mean()
eleventh_math = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')["math_score"].mean()
twelfth_math = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')["math_score"].mean()

math_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
math_scores = math_scores[['9th', '10th', '11th', '12th']]
math_scores.index.name = "School_name"

#show and format
math_scores.style.format({'9th': '{:.1f}', 
                          "10th": '{:.1f}', 
                          "11th": "{:.1f}", 
                          "12th": "{:.1f}"})


# ### Reading score by grade

# In[40]:


#creates grade level average math scores for each school 
ninth_math = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')["reading_score"].mean()
tenth_math = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')["reading_score"].mean()
eleventh_math = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')["reading_score"].mean()
twelfth_math = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')["reading_score"].mean()

reading_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
reading_scores = reading_scores[['9th', '10th', '11th', '12th']]
reading_scores.index.name = "School_name"

#show and format
reading_scores.style.format({'9th': '{:.1f}', 
                          "10th": '{:.1f}', 
                          "11th": "{:.1f}", 
                          "12th": "{:.1f}"})


# ### Scores by school spending

# In[41]:


# create spending bins
bins = [0, 584.999, 614.999, 644.999, 999999]
group_name = ['< $585', "$585 - 614", "$615 - 644", "> $644"]
school_data_complete['spending_bins'] = pd.cut(school_data_complete['budget']/school_data_complete['size'], bins, labels = group_name)

#group by spending
by_spending = school_data_complete.groupby('spending_bins')

#calculations
avg_math = by_spending['math_score'].mean()
avg_read = by_spending['reading_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()

            
# df build            
scores_by_spend = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
            
})
            
#reorder columns
scores_by_spend = scores_by_spend[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]

scores_by_spend.index.name = "Per Student Budget"
scores_by_spend = scores_by_spend.reindex(group_name)

#formating
scores_by_spend.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1%}', 
                              '% Passing Reading':'{:.1%}', 
                              'Overall Passing Rate': '{:.1%}'})


# ### Scores by school size

# In[42]:


# create size bins
bins = [0, 999, 1999, 99999999999]
group_name = ["Small (<1000)", "Medium (1000-2000)" , "Large (>2000)"]
school_data_complete['size_bins'] = pd.cut(school_data_complete['size'], bins, labels = group_name)

#group by spending
by_size = school_data_complete.groupby('size_bins')

#calculations 
avg_math = by_size['math_score'].mean()
avg_read = by_size['math_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()

            
# df build            
scores_by_size = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
            
})
            
#reorder columns
scores_by_size = scores_by_size[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]

scores_by_size.index.name = "Total Students"
scores_by_size = scores_by_size.reindex(group_name)

#formating
scores_by_size.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1%}', 
                              '% Passing Reading':'{:.1%}', 
                              'Overall Passing Rate': '{:.1%}'})


# ### Scores by school type

# In[43]:


# group by type of school
by_type = school_data_complete.groupby("type")

#calculations 
avg_math = by_type['math_score'].mean()
avg_read = by_type['math_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('type')['Student ID'].count()/by_type['Student ID'].count()
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('type')['Student ID'].count()/by_type['Student ID'].count()
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('type')['Student ID'].count()/by_type['Student ID'].count()

# df build            
scores_by_type = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall})
    
#reorder columns
scores_by_type = scores_by_type[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]
scores_by_type.index.name = "Type of School"


#formating
scores_by_type.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1%}', 
                              '% Passing Reading':'{:.1%}', 
                              'Overall Passing Rate': '{:.1%}'})

