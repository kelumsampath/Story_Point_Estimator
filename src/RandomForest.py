import csv

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

def write_csv_file(path, data_array,access_type):
    with open(path, access_type, newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in data_array:
            writer.writerow(row)

tfidf_value_matrix = pd.read_csv('./csv/5_tfidf_for_corpus.csv')

number_of_columns = len(tfidf_value_matrix.columns)

#tfidf value matrix(independent variables)
X = tfidf_value_matrix.iloc[:, 0:number_of_columns-1].values
#get story point list (dependent variable)
y = tfidf_value_matrix.iloc[:, number_of_columns-1].values

#separate training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


regressor = RandomForestRegressor(n_estimators=20, random_state=0)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

##read and estimate for new dataset
dataset = pd.read_csv('./csv/5_tfidf_for_corpus.csv')

Existing_text_features=sc.fit_transform(dataset.iloc[:, 0:number_of_columns-1].values)

text_score = regressor.predict(Existing_text_features)

#add new colums to write new values
dataset["test_score"]=text_score
dataset["test_score_round"]=np.rint(text_score)

write_csv_file('./csv/6_estimated_new_text_score.csv',dataset.to_numpy(),'w')

