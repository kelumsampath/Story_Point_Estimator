from src.Preprocess_TFIDF import get_word_root_format,create_document_term_matrix,read_csv_file,write_csv_file,filter_required_columns,refactor_dataset,get_dataset1
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np

#read data set from csv
dataset = read_csv_file('./csv/Prediction/New_data.csv')
#get only required fields from dataset
filtered_dataset = filter_required_columns(dataset)
#write filtered dataset into new csv
write_csv_file('./csv/Prediction/1_filtered_dataser.csv',filtered_dataset,'w')
#refactor input dataset as for different inputs
input_dataset = refactor_dataset(filtered_dataset)
#write dataset in input format
write_csv_file('./csv/Prediction/2_input_dataset.csv', input_dataset,'w')

#write title bar of input dataset1
write_csv_file('./csv/Prediction/3_input_dataset1.csv', [["Bug text", "Story point"]],'w')

#delete title bar from input_dataset
del input_dataset[0]

word_stem_string=[["Bug text root form", "Story point"]]

#consider only one bug at once
for bug in input_dataset:
    #get textual data from a bug-> bug set1=Bug text,Story point
    bug_set1 = get_dataset1(bug)
    #write bug set1 in 3_input_dataset1.csv
    write_csv_file('./csv/Prediction/3_input_dataset1.csv', [bug_set1], 'a')

    #get word list in root format (stem)
    word_stem_string.append([get_word_root_format(bug_set1[0]),bug_set1[1]])

#write title bar of input dataset1 root form
write_csv_file('./csv/Prediction/4_input_dataset1_rootform.csv', word_stem_string,'w')


bug_text_list=[]
story_point_list=[]
for bug in word_stem_string:
    bug_text_list.append(bug[0])
    story_point_list.append(bug[1])

#genarate and write tfidf values to corpus
term_matrix=create_document_term_matrix(bug_text_list)

#adding storypoint column to matrix
term_matrix["story_point"]=story_point_list

#remove first row( title values) and save as csv
term_matrix.drop(term_matrix.index[0]).to_csv (r'./csv/Prediction/5_tfidf_for_corpus.csv', index = False, header=True)

####text score prediction
sc = StandardScaler()

###read tf-idf value metrix from here
tfidf_value_matrix = pd.read_csv('./csv/Prediction/5_tfidf_for_corpus.csv')
number_of_columns = len(tfidf_value_matrix.columns)

###input fit to the model
Existing_text_features=sc.fit_transform(tfidf_value_matrix.iloc[:, 0:number_of_columns-1].values)

###load saved model
regressorModel = pickle.load(open('./Models/RandomForestModel.sav', 'rb'))
text_score = regressorModel.predict(Existing_text_features)

#add new colums to write new values
tfidf_value_matrix["test_score"]=text_score
tfidf_value_matrix["test_score_round"]=np.rint(text_score)

##store predicted values
write_csv_file('./csv/Prediction/6_estimated_new_text_score.csv',tfidf_value_matrix.to_numpy(),'w')