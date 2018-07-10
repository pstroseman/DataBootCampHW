
# coding: utf-8

# ### PyBank

# #### Tasks
# * Examine the budget_data.csv file.  Writedown the file location.
# * OPEN the budget_data.csv
# * CALCULATE the total number of months included in the dataset.
# * CALCULATE the total net amount of "Profit/Losses" over the entire period.
# * CALCULATE the average change in "Profit/Losses" between months over the entire period.
# * CALCULATE the greatest increse in profits (date and amount) over the entire period.
# * CALCULATE the greatest decreases in losses (date and amount) over the entire period
# 
# #### Note
# * Final scripts should print the analysis to the terminial as well as export a text files with the results.

# In[1]:


# Open the Budge_Data.CSV File

import csv
import os

current_work_directory = os.getcwd()    

# Return a string representing the current working directory.
print('Current work directory: {}'.format(current_work_directory))

# Make sure it's an absolute path.
abs_work_directory = os.path.abspath(current_work_directory)
print('Current work directory (full path): {}'.format(abs_work_directory))
print()

filename = 'budget_data.csv'

# Check whether file exists.

if not os.path.isfile(filename):

    # Stop with leaving a note to the user.
    print('It seems file "{}" does not exists in directory: "{}"'.format(filename, current_work_directory))


# In[17]:


import sys
import os

#Files to load and output
file_to_load = os.path.join("..", "PyBank", "budget_data.csv")
file_to_output = os.path.join("..", "PyBank", "budget_analysis.txt")


# In[6]:


# Define variables (Fiancial Parameters)

total_months = 0
month_of_change = []
net_change_list = []
greatest_increase = ['', 0]
greatest_decrease = ['', 99999999999999999999999]
total_net = 0


# In[7]:


# Read the csv and convert it into a list of dictionaries

with open (file_to_load) as financial_data:
    reader = csv.reader(financial_data)
    
    # Read the header row
    header = next(reader)
    
    # Extract first row to avoid appending to net_change_list
    first_row = next(reader)
    total_months = total_months + 1
    total_net = total_net + int(first_row[1])
    prev_net = int(first_row[1])
    
    for row in reader:
    
        #track the total
        total_months = total_months + 1
        total_net = total_net +int(row[1])
        
        #Track the net change
        net_change = int(row[1]) - prev_net
        prev_net = int(row[1])
        net_change_list = net_change_list + [net_change]
        month_of_change = month_of_change = [row[0]]
        
        #Calculate the greatest increase
        if net_change > greatest_increase[1]:
            greatest_increase[0] = row[0]
            greatest_increase[1] = net_change
            
        #Calculate the greatest decrease
        if net_change < greatest_decrease[1]:
            greatest_decrease[0] = row[0]
            greatest_decrease[1] = net_change
            
#Calculate the Average Net Change
net_monthly_avg = sum(net_change_list) / len(net_change_list)


# In[14]:


#Generate Output Summary

output = (
    f"\nFinancial Analysis\n"
    f"-----------------------------------\n"
    f"Total Months: {total_months}\n"
    f"Total: ${total_net}\n"
    f"Average Change: ${net_monthly_avg:.2f}\n"
    f"Greatest Increase in Profits: {greatest_increase[0]} (${greatest_increase[1]})\n"
    f"Greatest Decrease in Profits: {greatest_decrease[0]} (${greatest_decrease[1]})\n")
    
#Print the output (to terminal)

print (output)


# In[18]:


#Export the results to the text file
with open (file_to_output, "w") as txt_file:
    txt_file.write(output)

