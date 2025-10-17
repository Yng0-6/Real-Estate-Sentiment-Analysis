import pandas as pd
from snownlp import SnowNLP
import jieba.analyse
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import os
from time import strftime, localtime 

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False

# --- 1. Core Functions: Sentiment Analysis and Scoring ---

def sentiment_analyse(df_input):
    df = df_input.copy()
    df['Bullet Text'] = df['Bullet Text'].astype(str)
    score_list, tag_list = [], []  
    pos_count, neg_count, mid_count = 0, 0, 0
    for comment in df['Bullet Text'].tolist():
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
        score_list.append(sentiments_score)
        tag_list.append(tag)
    df['Sentiment Score'] = score_list 
    df['Determination Result'] = tag_list
    
    grp = df['Determination Result'].value_counts()
    print('Positive and Negative Review Statistics (Based on 0.5 Threshold):')
    print(grp)
    
    output_filename = 'Sentiment_Assessment_Results_All_Data.xlsx'
    df.to_excel(output_filename, index=False)
    
    return df

def generate_monthly_pi(df_analyzed):
    df = df_raw.copy()
    df['弹幕时间'] = pd.to_datetime(df['弹幕时间'])
    df['Month'] = df['弹幕时间'].dt.strftime('%Y-%m')
    df = df[(df['Month'] >= '2022-01') & (df['Month'] <= '2024-06')].copy()
    print("\n--- Calculating Monthly PI via Concatenated Text Sentiment ---")

    df_concatenated = (
        df.groupby('Month')['弹幕内容']
        .apply(lambda x: ' '.join(x.astype(str))) # Concatenate all bullet comments from that month into a single large string.
        .reset_index(name='Concatenated Text')
    )

    df_concatenated['PI'] = df_concatenated['Concatenated Text'].apply(
        lambda text: SnowNLP(text).sentiments
    )

    df_monthly_pi = df_concatenated[['Month', 'PI']]

    output_pi_file = 'Sentiment_Index.csv'
    df_monthly_pi.to_csv(output_pi_file, index=False)
    
    print(f"\nFinal Monthly PI Data Generated and Saved to '{output_pi_file}'.")
    
    return df_monthly_pi

if __name__ == '__main__':
    RAW_DATA_FILE = 'Bilibili bullet.csv' 
    COLUMN_MAPPING = {'弹幕内容': '弹幕内容', '弹幕时间': '弹幕时间'} 
    try:
        df_raw = pd.read_csv(RAW_DATA_FILE) 
        df_raw.rename(columns=COLUMN_MAPPING, inplace=True)
        df_raw.dropna(subset=['弹幕内容'], inplace=True)
    except FileNotFoundError:
        print(f"Fatal Error: Raw data file ({RAW_DATA_FILE}) not found. Cannot proceed.")
        exit()
    except Exception as e:
        print(f"Fatal Error reading data: {e}. Check file format.")
        exit()
        
    print(f"Total entries loaded: {len(df_raw)}")
    df_analyzed = sentiment_analyse(df_input=df_raw)
    
    df_monthly_pi = generate_monthly_pi(df_raw)

    v_cmt_str = ' '.join(df_raw['弹幕内容'].astype(str).tolist())
    
    print("\n--- Top 20 High-Frequency Words ---")
    
    keywords_top20 = jieba.analyse.extract_tags(v_cmt_str, withWeight=True, topK=20)
    pprint(keywords_top20)
    with open('TOP20_High-Frequency_Words.txt', 'w', encoding='utf-8') as f:
        f.write(str(keywords_top20))
