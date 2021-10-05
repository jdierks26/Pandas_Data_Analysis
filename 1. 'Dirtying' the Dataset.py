import pandas as pd

# According to Hadley Wickham, publisher of 'Tidy Data' in the Journal of Statistical Software, this dataset is 'tidy.'
# This mean that our data is organized in a way that is ready for analysis. I would like to 'dirty' this dataset:
# create artificial problems that someone might run into while cleaning data.
# [Link to Hadley's paper: https://vita.had.co.nz/papers/tidy-data.pdf]

# Loading our dataset into a variable called 'df'
df = pd.read_csv('Car details v3.csv')

# ----------------------------------------------------------------------------------------------------------------------
# Goal 1: Create a problem where a column's values are stored inside multiple column headers, instead of one neat column
# ----------------------------------------------------------------------------------------------------------------------

# In Hadley's paper, she lists a few common problems seen in 'untidy' datasets. The first problem she lists entails
# column headers storing values, not variable names. Let's try to emulate this by turning
# the 'fuel' column into several columns, and using TRUE and FALSE instead, so it'll look like this:
# CNG	Diesel	LPG	    Petrol
# FALSE	TRUE	FALSE	FALSE
# FALSE	TRUE	FALSE	FALSE
# FALSE	FALSE	FALSE	TRUE
# FALSE	TRUE	FALSE	FALSE
# FALSE	FALSE	FALSE	TRUE

# Recording information like this is likely rare, but is a good example to showcase some skills

# Since we want a new column for each unique variable in fuel, we need to use a set. Sets will ignore duplicate
# entries, leaving us with each unique value
set1 = set()

# Here we are iterating through every index in 'fuel' and adding it's value to our new set
for i in df.index:
    set1.add(df.loc[i, 'fuel'])

# Here we are using a FOR loop to create a new column for each unique value in our set. We also need to convert our
# set into a list so we can index for a future for loop

mylist = list()

for x in set1:
    df[x] = 0
    mylist.append(x)

# I am using a counter to cycle through the indexes of our list of unique variables in 'fuel' in the for loop below, so
# that each unique entry can be called upon. Sets are unordered so they cannot be indexed, which is why we need a list

count = 0

# This nested FOR loop will, for every new column generated out of our set, iterate through the rows and assign TRUE
# if the values match, and FALSE if not

for x in mylist:
    for i in df.index:
        if df.loc[i, 'fuel'] == mylist[count]:
            df.loc[i, mylist[count]] = True
        else:
            df.loc[i, mylist[count]] = False
    count += 1

# Dropping our old 'fuel' column
df = df.drop(columns='fuel')

# ----------------------------------------------------------------------------------------------------------------------
# Goal 2: Create a problem where 2 variables are stored into one column
# ----------------------------------------------------------------------------------------------------------------------

# Let's say 'name' and 'year' were recorded together in a column called 'model', so the first index looked like
# this: 2014 Maruti Swift Dzire VDI. This could be a problem if we want to control for the year later in our
# analysis

# We can use a FOR loop to iterate through each index, find the values in 'name' and 'year' for each index,
# and combine them into a new column called 'model'
for i in df.index:
    df.loc[i, 'model'] = str(df.loc[i, 'year']) + ' ' + str(df.loc[i, 'name'])

# Dropping the original columns
df = df.drop(columns=['name','year'])

# ----------------------------------------------------------------------------------------------------------------------
# Goal 3: Create a problem where a column is recorded inconsistently
# ----------------------------------------------------------------------------------------------------------------------

# Let's say that the 'owner' column was recorded in two different formats, and about 1/5 of the columns are not recorded
# correctly. Currently, the 'owner' column has these unique values:
# 'First Owner', 'Second Owner', 'Third Owner', 'Test Drive Car', 'Fourth & Above Owner'

# Let's say that someone recorded a part of the 'owner' column like so:
# Test Drive Car = 0
# First Owner = 1
# Second Owner = 2
# Third Owner = 3
# Fourth & Above Owner = 4+

# We can use a FOR loop to scan through every 5th index of df and change the value in 'owner' to its equivalent numeric
# value

for i in df.index[::5]:
    if df.loc[i,'owner'] == 'First Owner':
        df.loc[i,'owner'] = 1
    elif df.loc[i,'owner'] == 'Second Owner':
        df.loc[i, 'owner'] = 2
    elif df.loc[i,'owner'] == 'Third Owner':
        df.loc[i, 'owner'] = 3
    elif df.loc[i,'owner'] == 'Fourth & Above Owner':
        df.loc[i, 'owner'] = "4+"
    else:
        df.loc[i, 'owner'] = 0

# ----------------------------------------------------------------------------------------------------------------------
# Goal 4: Split the dataset into 2 csv files
# ----------------------------------------------------------------------------------------------------------------------

# Let's say that this dataset was actually recorded in two different CSV files, and we need to join them together. Let's
# say that df1 contained the model, selling price, and mileage, and df2 contained model and everything else.
# We can split the dataset like so:

df1 = df[['model', 'selling_price', 'mileage']]

df1.to_csv('df1.csv')

df2 = df[['model', 'km_driven', 'seller_type', 'transmission', 'owner', 'engine', 'max_power', 'torque',
          'seats', 'LPG', 'CNG', 'Petrol', 'Diesel']]

df2.to_csv('df2.csv')

