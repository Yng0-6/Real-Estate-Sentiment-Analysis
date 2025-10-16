import pandas as pd  # 数据分析库
from snownlp import SnowNLP  # 中文情感分析库
from wordcloud import WordCloud  # 绘制词云图
from pprint import pprint  # 美观打印
import jieba.analyse  # jieba分词
from PIL import Image  # 读取图片
import numpy as np  # 将图片的像素点转换成矩阵数据
import matplotlib.pyplot as plt  # 画图

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['Arial']  # 显示中文标签  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# 情感分析打标
def sentiment_analyse(v_cmt_list):
	"""
	情感分析打分
	:param v_cmt_list: 需要处理的评论列表
	:return:
	"""
	score_list = []  # 情感评分值
	tag_list = []  # 打标分类结果
	pos_count = 0  # 计数器-积极
	neg_count = 0  # 计数器-消极
	mid_count = 0  # 计数器-中性
	for comment in v_cmt_list:
		tag = ''
		sentiments_score = SnowNLP(comment).sentiments
		if sentiments_score < 0.5:
			tag = '消极'
			neg_count += 1
		elif sentiments_score > 0.5:
			tag = '积极'
			pos_count += 1
		else:
			tag = '中性'
			mid_count += 1
		score_list.append(sentiments_score)  # 得分值
		tag_list.append(tag)  # 判定结果
	df['情感得分'] = score_list
	df['分析结果'] = tag_list
	grp = df['分析结果'].value_counts()
	print('正负面评论统计：')
	print(grp)
	df.to_excel('22情感评分结果.xlsx', index=None)
	print('情感分析结果已生成：22情感评分结果.xlsx')



if __name__ == '__main__':
	df = pd.read_excel('22.xlsx')  # 读取excel
	v_cmt_list = df['弹幕内容'].values.tolist()  # 评论内容列表
	print('length of v_cmt_list is:{}'.format(len(v_cmt_list)))
	v_cmt_list = [str(i) for i in v_cmt_list]  # 数据清洗-list所有元素转换成字符串
	v_cmt_str = ' '.join(str(i) for i in v_cmt_list)  # 评论内容转换为字符串
	# 1、情感分析打分
	sentiment_analyse(v_cmt_list=v_cmt_list)
	# 2、用jieba统计弹幕中的top10高频词
	keywords_top20 = jieba.analyse.extract_tags(v_cmt_str, withWeight=True, topK=20)
	pprint(keywords_top20)
	with open('22_TOP20高频词.txt', 'w') as f:
		f.write(str(keywords_top20))
	
