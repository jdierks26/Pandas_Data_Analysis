import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------
# Goal 1: Merge the two csv files
# ----------------------------------------------------------------------------------------------------------------------

df1 = pd.read_csv('df1.csv')
df2 = pd.read_csv('df2.csv')

new_df = pd.merge(df1, df2)

new_df.to_csv('new_df.csv')

df = pd.read_csv('new_df.csv')

# ----------------------------------------------------------------------------------------------------------------------
# Goal 2: Fix the problem where multiple column headers are values, not variables
# ----------------------------------------------------------------------------------------------------------------------

# We can use another nested FOR loop to iterate through each new column, and if the value is TRUE, return the header
# of the column into that index in a new column called 'fuel'

for x in ['CNG', 'Diesel', 'LPG', 'Petrol']:
    for i in df.index:
        if df.loc[i, x]:
            df.loc[i, 'fuel'] = x

df = df.drop(columns=['CNG', 'Diesel', 'LPG', 'Petrol'])

# ----------------------------------------------------------------------------------------------------------------------
# Goal 3: Fix the problem where 2 variables are stored into one column
# ----------------------------------------------------------------------------------------------------------------------

# We can declare a new list of columns and use .split to separate the 'model' column at the first space and use the two
# outputs to fill the new columns

df[['year','name']] = df['model'].str.split(" ",1,expand=True)

df = df.drop(columns=['model'])

# ----------------------------------------------------------------------------------------------------------------------
# Goal 4: Fix the problem where a column is recorded inconsistently
# ----------------------------------------------------------------------------------------------------------------------

# We can use a for loop and if statements to re-convert our numbers to the text equivalent

for i in df.index:
    if df.loc[i,'owner'] == str(1):
        df.loc[i,'owner'] = 'First Owner'
    elif df.loc[i,'owner'] == str(2):
        df.loc[i, 'owner'] = 'Second Owner'
    elif df.loc[i,'owner'] == str(3):
        df.loc[i, 'owner'] = 'Third Owner'
    elif df.loc[i,'owner'] == "4+":
        df.loc[i, 'owner'] = 'Fourth & Above Owner'
    elif df.loc[i, 'owner'] == str(0):
        df.loc[i, 'owner'] = 'Test Drive Car'

# ----------------------------------------------------------------------------------------------------------------------
# Goal 5: Perform various data manipulation techniques, such as applying functions, filtering, sorting, etc.
# ----------------------------------------------------------------------------------------------------------------------

# Let's say we needed to make the following (arbitrary) changes to our dataset before we perform analysis:
# 1. Remove all entries that don't have complete data
# 2. Remove the 'max power' column
# 3. Remove all entries where 'name' contains 'renault'
# 4. Convert 'mileage' and 'km_driven' from metric to imperial units
# 5. Create a new column called 'price_per_mile' that takes selling_price/miles_driven
# 6. Convert 'selling_price' from rupees to dollars

# 1. Remove all entries that don't have complete data
# Using .dropna we can remove any rows that have missing or NaN values. There are multiple ways of dealing with
# NaN values, but this is the easiest solution for this dataset since we have so many observations. For a smaller
# dataset we might want to fill in NaN values with a median calculation

df = df.dropna()

# 2. Remove the 'max power' column
# Using .drop we can remove the 'max power' column

df = df.drop(columns='max_power')

# 3. Remove all entries where 'name' contains 'renault'
# Using .str.contains and .loc to filter out any entries that contain "renault"

df = df.loc[~df['name'].str.contains('Renault')]

# 4. Convert 'mileage' and 'km_driven' from metric to imperial units
# We can use a FOR loop to iterate through each index of 'km_driven' and multiply it by .62137 to get our miles, then
# write over the pre-existing value

for i in df.index:
    df.loc[i, 'km_driven'] = round((df.loc[i, 'km_driven'] * 0.62137),0)

df['miles_driven'] = df['km_driven']

df = df.drop(columns='km_driven')

# 4.2
# Converting kmpl to mpg is a bit trickier since we first need to split the column to extract the number. Once we do
# that, we can divide our kmpl number, after coverting it to a float number, by the appropriate conversion rate, then
# round off the number and convert it to a string so we can concatenate "mpg"

df['mileage'] = df['mileage'].str.split(' ').str[0]

for i in df.index:
    df.loc[i,'mileage'] = str(round((float(df.loc[i,'mileage'])/0.425143707),2)) + "mpg"

# 5. Create a new column called 'price_per_mile' that takes selling_price/miles_driven

for i in df.index:
    df.loc[i, 'price_per_mile'] = "$" + str(round(df.loc[i, 'selling_price']/df.loc[i,'miles_driven'],2))

# 6.
# Convert selling_price from India's rupee to US dollar

for i in df.index:
    df.loc[i,'selling_price'] = df.loc[i,'selling_price'] * 0.0137001

# Re-ordering columns in a logical manner

df = df[['name', 'year', 'miles_driven', 'price_per_mile', 'mileage', 'selling_price', 'seller_type', 'owner',
         'transmission', 'engine', 'torque', 'seats', 'fuel']]

df = df.sort_values("selling_price",ascending= False)

df.to_csv('check.csv')