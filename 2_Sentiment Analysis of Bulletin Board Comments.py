import pandas as pd  
from snownlp import SnowNLP  
from wordcloud import WordCloud  
from pprint import pprint  
import jieba.analyse 
from PIL import Image  
import numpy as np  
import matplotlib.pyplot as plt  


plt.rcParams['font.sans-serif'] = ['Arial']  
plt.rcParams['axes.unicode_minus'] = False  

def sentiment_analyse(v_cmt_list):
	score_list = []  # Sentiment Score
	tag_list = []  # Labeling Classification Results
	pos_count = 0  # Counter - Positive
	neg_count = 0  # Counter - Negative
	mid_count = 0  # Counter - Neutral
	for comment in v_cmt_list:
		tag = ''
		sentiments_score = SnowNLP(comment).sentiments
		if sentiments_score < 0.5:
			tag = 'Negative'
			neg_count += 1
		elif sentiments_score > 0.5:
			tag = 'Positive'
			pos_count += 1
		else:
			tag = 'Neutral'
			mid_count += 1
		score_list.append(sentiments_score)  # Score
		tag_list.append(tag)  # Determination Result
	df['Sentiment Score'] = score_list
	df['Determination Result'] = tag_list
	grp = df['Determination Result'].value_counts()
	print('Positive and Negative Review Statistics:')
	print(grp)
	df.to_excel('2022 Emotional Assessment Results.xlsx', index=None)
	print('Sentiment analysis results have been generated: 2022 Sentiment Score Results.xlsx')



if __name__ == '__main__':
	df = pd.read_excel('2022 Emotional Assessment Results')  # Read Excel
	v_cmt_list = df['Bullet text'].values.tolist()  # List of Comment Content
	print('length of v_cmt_list is:{}'.format(len(v_cmt_list)))
	v_cmt_list = [str(i) for i in v_cmt_list]  # Data Cleaning - Convert all elements in the list to strings
	v_cmt_str = ' '.join(str(i) for i in v_cmt_list)  # Convert comment content to a string
	# 1. Sentiment Analysis Scoring
	sentiment_analyse(v_cmt_list=v_cmt_list)
	# 2. Use Jieba to count the top 10 most frequent words in bullet comments.
	keywords_top20 = jieba.analyse.extract_tags(v_cmt_str, withWeight=True, topK=20)
	pprint(keywords_top20)
	with open('22_TOP20 High-Frequency Words.txt', 'w') as f:
		f.write(str(keywords_top20))
	
