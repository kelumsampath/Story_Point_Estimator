import pandas as pd
import matplotlib.pyplot as plt

input_dataset2= pd.read_csv("./csv/Prediction/9_input_datset2.csv")


plt.scatter(input_dataset2['previous_story_point'], input_dataset2['estimated_test_score'], color='green')
plt.title('Story point vs Text score', fontsize=14)
plt.ylabel('Text Score', fontsize=14)
plt.xlabel('Story point', fontsize=14)
plt.grid(True)
plt.show()

plt.scatter(input_dataset2['previous_story_point'], input_dataset2['Number of developers'], color='red')
plt.title('Story point vs Number of developers', fontsize=14)
plt.ylabel('Number of developers', fontsize=14)
plt.xlabel('Story point', fontsize=14)
plt.grid(True)
plt.show()

plt.scatter(input_dataset2['previous_story_point'], input_dataset2['Number of comments'], color='blue')
plt.title('Story point vs Number of comments', fontsize=14)
plt.ylabel('Number of comments', fontsize=14)
plt.xlabel('Story point', fontsize=14)
plt.grid(True)
plt.show()