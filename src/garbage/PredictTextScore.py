import json
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.Preprocess_TFIDF import get_word_root_format,create_document_term_matrix,read_csv_file,write_csv_file

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

sc = StandardScaler()

# Opening JSON file
file = open('./csv/Prediction/New_data.json',)

#read new data set from Json file
New_data_values =json.load(file)

##extract one bug from New_data_values
New_Bug=New_data_values[0]

##get title+description
Text_data=New_Bug['Summary']+New_Bug['Description']

Text_data_Root_Format=get_word_root_format(Text_data)

#genarate and write tfidf values to corpus
term_matrix=create_document_term_matrix([Text_data_Root_Format])

# print(term_matrix.columns[1])
# print(term_matrix.values[0][2])

header=read_csv_file('../csv/5_tfidf_for_corpus.csv')[0]

Text_Feature_Matrix=[header]

number_of_columns=len(header)

Text_Feature_Matrix.append(zerolistmaker(number_of_columns))
# print(type(Text_Feature_Matrix))
# print(type(term_matrix))
products_list = [term_matrix.columns.values.tolist()] + term_matrix.values.tolist()
# print(type(products_list))
# print(term_matrix)
# print(products_list)
# print(Text_Feature_Matrix)

list=[[],[]]
list[0]=products_list[0]+Text_Feature_Matrix[0]
list[1]=products_list[1]+Text_Feature_Matrix[1]
# print('SSSSSSSSSSSSS')
# print(list)
for word in products_list[0]:
    if word in Text_Feature_Matrix[0]:
        Text_Feature_Matrix[1][Text_Feature_Matrix[0].index(word)]=products_list[1][products_list[0].index(word)]

print(Text_Feature_Matrix)
regressorModel = pickle.load(open('../Models/RandomForestModel.sav', 'rb'))
# print(Text_Feature_Matrix)


# ####Prediction
# write_csv_file('./csv/Prediction/New_data_2.csv',Text_Feature_Matrix,'w')
#
# # text_score = regressorModel.predict(Text_Feature_Matrix)
#
#
# dataset = pd.read_csv('./csv/Prediction/New_data_2.csv')
#
# Existing_text_features=sc.fit_transform(dataset.iloc[:, 0:number_of_columns-1].values)
#
# text_score = regressorModel.predict(Existing_text_features)
# print(text_score)
# #add new colums to write new values
# dataset["test_score"]=text_score
# dataset["test_score_round"]=np.rint(text_score)

write_csv_file('./csv/Prediction/New_data_3.csv',dataset.to_numpy(),'w')




