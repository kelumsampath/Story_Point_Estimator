import csv
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

ps = PorterStemmer()

#stop words in english lanugage
stop_words = set(stopwords.words('english'))

def read_csv_file(path):
    with open(path, encoding="utf8") as csv_file:
        ss= csv.reader(csv_file, delimiter=',')
        data_array=[]
        for data_row in ss:
            data_array.append(data_row)
        return data_array

def write_csv_file(path, data_array,access_type):
    with open(path, access_type, newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in data_array:
            writer.writerow(row)

def filter_required_columns(dataset):
    line_count = 0
    summary_column = 0
    description_column = 0
    assignee_column = 0
    comment_column = []
    storypoint_column = 0
    filtered_dataset = []
    for data_row in dataset:
        if line_count == 0:
            column_count = 0
            for column_name in data_row:
                if column_name == "Summary":
                    summary_column = column_count
                elif column_name == "Description":
                    description_column = column_count
                elif column_name == "Assignee":
                    assignee_column = column_count
                elif "Story Points" in column_name:
                    storypoint_column = column_count
                elif column_name == "Comment":
                    comment_column.append(column_count)
                column_count += 1
        filtered_dataset.append([data_row[summary_column]] + [data_row[description_column]] + [data_row[assignee_column]] + [data_row[storypoint_column]] + [data_row[i] for i in comment_column])
        line_count += 1
    return filtered_dataset

#this funtion is to make dataset as input format (summary,description, number of devolopers, number of comments)
def refactor_dataset(filtered_dataset):
    input_processed_dataset = [["Summary", "Description", "Number of developers", "Number of comments", "Story point"]]
    row_count = 0
    for row in filtered_dataset:
        single_entry = []
        if row_count != 0:
            single_entry.append(row[0])
            single_entry.append(row[1])
            assignee_count = 0
            if row[2] != "":
                assignee_count = row[2].count(",") + 1
            single_entry.append(assignee_count)
            comment_list = row[4: None]
            comment_count = 0
            for comment in comment_list:
                if comment != '':
                    comment_count += 1
            single_entry.append(comment_count)
            single_entry.append(row[3])
            input_processed_dataset.append(single_entry)
        row_count += 1
    # remove garbage values
    input_data_row_count = 0
    temp_input_processed_dataset = input_processed_dataset
    for input_data_row in temp_input_processed_dataset:
        if input_data_row[2] == 0 and input_data_row[3] == 0 and input_data_row[4] == '':
            del input_processed_dataset[input_data_row_count]
        input_data_row_count += 1
    return input_processed_dataset

#extract summary&description as bug description and storypoint
def get_dataset1(bug):
    return [bug[0] + " " + bug[1], bug[4]]

def get_word_root_format(bug_text):
    # tokenize text
    words_list = word_tokenize(bug_text)
    # remove stop words from words list
    filtered_sentence = [w for w in words_list if not w in stop_words]
    word_stem_list=[]
    for w in filtered_sentence:
        word_stem_list.append(ps.stem(w))
    #convert list into string
    root_form_string = ' '.join([str(elem) for elem in word_stem_list])
    return root_form_string

###main###

#read data set from csv
dataset = read_csv_file('./../dataset/spring.csv')
#get only required fields from dataset
filtered_dataset = filter_required_columns(dataset)
#write filtered dataset into new csv
write_csv_file('./csv/1_filtered_dataser.csv',filtered_dataset,'w')
#refactor input dataset as for different inputs
input_dataset = refactor_dataset(filtered_dataset)
#write dataset in input format
write_csv_file('./csv/2_input_dataset.csv', input_dataset,'w')

#write title bar of input dataset1
write_csv_file('./csv/3_input_dataset1.csv', [["Bug text", "Story point"]],'w')

#delete title bar from input_dataset
del input_dataset[0]

word_stem_string=[["Bug text root form", "Story point"]]

#consider only one bug at once
for bug in input_dataset:
    #get textual data from a bug-> bug set1=Bug text,Story point
    bug_set1 = get_dataset1(bug)
    #write bug set1 in 3_input_dataset1.csv
    write_csv_file('./csv/3_input_dataset1.csv', [bug_set1], 'a')

    #get word list in root format (stem)
    word_stem_string.append([get_word_root_format(bug_set1[0]),bug_set1[1]])

#write title bar of input dataset1 root form
write_csv_file('./csv/4_input_dataset1_rootform.csv', word_stem_string,'w')






