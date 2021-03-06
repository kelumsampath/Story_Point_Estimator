import csv
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

ps = PorterStemmer()

with open('./../dataset/spring.csv',  encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    summary_column=0
    description_column=0
    assignee_column=0
    comment_column=[]
    storypoint_column=0
    filtered_dataset=[]
    for data_row in csv_reader:
        if line_count == 0:
            column_count=0
            for column_name in data_row:
                if column_name == "Summary" :
                    summary_column=column_count
                elif column_name == "Description":
                    description_column=column_count
                elif column_name == "Assignee":
                    assignee_column=column_count
                elif "Story Points" in column_name:
                    storypoint_column=column_count
                elif column_name == "Comment":
                    comment_column.append(column_count)
                column_count +=1
        filtered_dataset.append([data_row[summary_column]] +[data_row[description_column]] +[data_row[assignee_column]]+[data_row[storypoint_column]]+ [data_row[i] for i in comment_column])
        line_count += 1
        ##print filtered dataset
    # for row in filtered_dataset:
    #     print(row)
    # print(f'Processed {line_count} lines.')

with open('filtered_dataset.csv', 'w',newline='',encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in filtered_dataset:
        writer.writerow(row)
with open('input_processed_dataset.csv', 'w',newline='',encoding="utf-8") as f:
    writer = csv.writer(f)
    input_processed_dataset=[["Summary","Description","Number of developers","Number of comments","Story point"]]
    row_count=0
    for row in filtered_dataset:
        single_entry = []
        if row_count!=0:
            single_entry.append(row[0])
            single_entry.append(row[1])
            assignee_count=0
            if row[2]!="":
                assignee_count=row[2].count(",")+1
            single_entry.append(assignee_count)
            comment_list = row[4: None]
            comment_count=0
            for comment in comment_list:
                if comment != '':
                    comment_count+=1
            single_entry.append(comment_count)
            single_entry.append(row[3])
            ##print(single_entry)
            input_processed_dataset.append(single_entry)
        row_count +=1

    #remove garbage values
    input_data_row_count=0
    temp_input_processed_dataset=input_processed_dataset
    for input_data_row in temp_input_processed_dataset:
        if input_data_row[2]==0 and input_data_row[3]==0 and input_data_row[4]=='':
            del input_processed_dataset[input_data_row_count]
        input_data_row_count +=1

    # #print input processed datatset
    # for input_data_row in input_processed_dataset:
    #     print(input_data_row)

    for input_data_row in input_processed_dataset:
        writer.writerow(input_data_row)

    #combile title and description
with open('input_set1.csv', 'w',newline='',encoding="utf-8") as f:
    writer = csv.writer(f)
    input_dataset1=[["Summary & Description","Story point"]]

    for row_data in input_processed_dataset:
        input_dataset1.append([row_data[0]+" "+row_data[1],row_data[4]])

    for input_set1 in input_dataset1:
        #print(input_set1)
        writer.writerow(input_set1)

    #tokenize text (title+description)
    words_list = word_tokenize(input_dataset1[2][0])

    #stop words in english lanugage
    stop_words = set(stopwords.words('english'))

    #remove stop words from words list
    filtered_sentence = [w for w in words_list if not w in stop_words]

    filtered_sentence = []

    for w in words_list:
        if w not in stop_words:
            filtered_sentence.append(w)

    #print(words_list)
    #print(filtered_sentence)

    for w in filtered_sentence:
        print(ps.stem(w))
