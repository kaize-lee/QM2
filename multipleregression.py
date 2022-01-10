# -*- coding: utf-8 -*-
"""MultipleRegression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GdPKURFGrJj2Ol-c6-iqUt3dfnlTiTSc
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn.metrics import r2_score

# we upload each csv file into a dataframe

dependent_variable = pd.read_csv('/content/drive/MyDrive/ColabNotebooks/ViolentCrimesProject/violentcrimepb.csv')

independent_variable1 = pd.read_csv('/content/drive/MyDrive/ColabNotebooks/ViolentCrimesProject/incomes.csv')

independent_variable2 = pd.read_csv('/content/drive/MyDrive/ColabNotebooks/ViolentCrimesProject/pubclub.csv')

independent_variable3 = pd.read_csv('/content/drive/MyDrive/ColabNotebooks/ViolentCrimesProject/stops.csv')

independent_variable4 = pd.read_csv('/content/drive/MyDrive/ColabNotebooks/ViolentCrimesProject/Happiness.csv')

independent_variable5 = pd.read_csv('/content/drive/MyDrive/ColabNotebooks/ViolentCrimesProject/officersper1000a.csv')

"""## Multiple Linear Regression

Following the analysis of correlation between each DV-IV pair, but also of multicollinearity between the IV, we are keeping:
- pubs and clubs for 2012 and 2018 (*x2*)
- stop and search for 2012 and 2018 (*x3*)
- happiness for 2012 (*x4*)
- police for 2012 and 2018 (*x5*)
"""

from sklearn import linear_model
# this is the library we will be using for the regression

"""### for 2012"""

# we select the correct year from each previous dataframe created
dependent_variable_2012 = dependent_variable.loc[:,["Borough","VIOLENT CRIMES PER 1000 PEOPLE 2012"]]
dependent_variable_2012

independent_variable2_2012 = independent_variable2.loc[:,"2012"]
independent_variable2_2012

independent_variable3_2012 = independent_variable3.loc[:,"2012"]
independent_variable3_2012.head()

independent_variable4_2012 = independent_variable4.loc[:,"2012"]
independent_variable4_2012.head()

independent_variable5_2012 = independent_variable5.loc[:,"2012"]
independent_variable5_2012

# creating a dataframe with all the data for the regression
# this is necessary for the library tool we are using

# we can use concat because all the dataframes have the same number of indexes
# we need to specify axis=1
# otherwise the columns will not be concatenated next to each other but all in the same column

multiple_regression_df = pd.concat([dependent_variable_2012, independent_variable2_2012, independent_variable3_2012, independent_variable4_2012, independent_variable5_2012], axis=1)
multiple_regression_df

# adding the correct column names to the regression dataframe
# for clearer comprehension

multiple_regression_df.columns = ('Borough', 'VIOLENT CRIMES PER 1000 PEOPLE 2012', 'Nightclubs and pubs', 'Stops and search', 'Happiness Levels', 'Number of Police Officers')
multiple_regression_df
# now all of the data we need for the multiple regression is in the same df

# defining the variables on the x-axis and the y-axis
# it is a convention in Python to use X and y

X_2012 = multiple_regression_df[['Nightclubs and pubs', 'Stops and search', 'Happiness Levels', 'Number of Police Officers']]
y_2012 = multiple_regression_df['VIOLENT CRIMES PER 1000 PEOPLE 2012']

X_2012

y_2012

# we use statsmodel library
# also gives R-squared and other important values

import statsmodels.api as sm

X_2012 = sm.add_constant(X_2012) 
# this is to add the constant in the equation (Y-intercept)
 
model_2012 = sm.OLS(y_2012, X_2012).fit()
# this is the fit regression model
 
print_model = model_2012.summary()
# this is to print the results
print(print_model)

"""### for 2018"""

# we repeat the exact same process as for 2012

dependent_variable_2018 = dependent_variable.loc[:,["Borough","VIOLENT CRIMES PER 1000 PEOPLE 2018"]]

independent_variable2_2018 = independent_variable2.loc[:,"2018"]

independent_variable3_2018 = independent_variable3.loc[:,"2018"]

independent_variable5_2018 = independent_variable5.loc[:,"2018"]

multiple_regression_2018_df = pd.concat([dependent_variable_2018, independent_variable2_2018, independent_variable3_2018, independent_variable5_2018], axis=1)

multiple_regression_2018_df.columns = ('Borough', 'VIOLENT CRIMES PER 1000 PEOPLE 2012', 'Nightclubs and pubs', 'Stops and search', 'Number of Police Officers')
multiple_regression_2018_df

X_2018 = multiple_regression_2018_df[['Nightclubs and pubs', 'Stops and search', 'Number of Police Officers']]
y_2018 = multiple_regression_2018_df['VIOLENT CRIMES PER 1000 PEOPLE 2012']

X_2018 = sm.add_constant(X_2018) 
 
model_2018 = sm.OLS(y_2018, X_2018).fit() 
 
print_model = model_2018.summary()
print(print_model)



"""### Visualisation of results"""

# let's create a grouped bar graph comparing 2012 and 2018
# that shows the coefficients of each independent variable

# first let's retrieve the coefficients from the model summary
# with params function of the statsmodel

params_2012 = model_2012.params
params_2018 = model_2018.params

coefs_2012 = params_2012.drop('const')
# to get rid of the constant that we are not showing in the visualisation

coefs_2012.columns = ('Independent Variables', 'Coefficients')
# add column names

print(coefs_2012)

coefs_2018 = params_2018.drop('const')
print(coefs_2018)

# let's create a dictionary
coefs = {'Nightclubs and pubs': [-1.043849, 7.379857],
         'Stops and search': [0.120139, 0.476657],
         'Number of Police Officers': [-0.522475, -1.147016]}
# we are not putting happiness levels
# as having it only for 2012 and not 2018 would create confusion

# and now let's put this dict into a dataframe
coefs = pd.DataFrame([['2012', -1.043849, 0.120139, -0.522475], ['2018', 7.379857, 0.476657, -1.147016]], columns=['Year', 'Nightclubs and pubs', 'Stops and search', 'Number of Police Officers'])

coefs

# now we can plot the grouped bar graph
coefs.plot(x='Year', kind='bar',stacked=False, title='Grouped Bar Graph of Regression Coefficients', ylabel='Coefficient')
# stacked=False because we want to keep the results separated

