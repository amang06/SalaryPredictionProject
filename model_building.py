import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('eda_data.csv')

# choose relevant columns
df.columns

df_model = df[['avg_salary','Rating', 'Size', 'Type of ownership', 'Industry','Sector', 'Revenue','hourly', 'employer provided',
             'job_state','age', 'python_yn', 'spark_yn', 'aws_yn', 'excel_yn','job_simp', 'seniority', 'desc_len']]

# get dummy data
df_dum = pd.get_dummies(df_model)

# train test split
from sklearn.model_selection import train_test_split
X = df_dum.drop('avg_salary', axis=1)
y = df_dum.avg_salary.values
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=42)

# multiple linear regression

#statsmodel ols regression
import statsmodels.api as sm
X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

# sklearn regression model
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)
np.mean(cross_val_score(lm, X_train, y_train, scoring = 'neg_mean_absolute_error')) #-13.899

# lasso regression
lm_l = Lasso(alpha=0.014)
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l, X_train, y_train, scoring = 'neg_mean_absolute_error'))
alpha = []
error = []

for i in range (1,100):
    alpha.append(i/1000)
    lml = Lasso(alpha=(i/1000))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring = 'neg_mean_absolute_error')))
    
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]
#    alpha      error
# 13  0.014 -13.430872

# random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()


np.mean(cross_val_score(rf, X_train, y_train, scoring = 'neg_mean_absolute_error')) #-8.860477870765761

# tune models GridsearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10)}

gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error')
gs.fit(X_train,y_train)
gs.best_score_
gs.best_estimator_

# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test) 

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)

import pickle
pick = {'model':gs.best_estimator_}
pickle.dump(pick, open('model_file'+".p","wb"))

file_name = "model_file.p"
with open(file_name,'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']
    
model.predict(X_test.iloc[0].values.reshape(1,-1))

X_test.iloc[0].values.reshape(1,-1)
