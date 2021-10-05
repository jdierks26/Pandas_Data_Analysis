import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model, datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Loading in our dataset
df = pd.read_csv('check.csv')

# Declaring our dependent variable for our test split
y = df.selling_price

# Declaring our training variables and test variables using an 80/20 split
X_train, X_test, y_train, y_test = train_test_split(df[['miles_driven','year']], y, test_size=0.2)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

# Fitting our linear regression with our training variables, then using that model to predict on our test variables
lm = linear_model.LinearRegression()
model = lm.fit(X_train, y_train)
predictions = lm.predict(X_test)

print(predictions)

# Plotting our test (or true) variable values vs. our predicted values
plt.scatter(y_test, predictions)
plt.xlabel("True Values")
plt.ylabel("predictions")

# Here we can compute an accuracy score for the model we created. With a score of .1698, our model isn't the most
# accurate

r2 = metrics.r2_score(y, predictions)
print(r2)