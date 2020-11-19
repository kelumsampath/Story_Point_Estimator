import csv

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
    for row in filtered_dataset:
        print(row)
    print(f'Processed {line_count} lines.')

with open('filtered_dataset.csv', 'w',newline='',encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in filtered_dataset:
        writer.writerow(row)

