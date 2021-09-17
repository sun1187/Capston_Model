# -*- coding: utf-8 -*-
"""ver6 level2 predict.ipynb"""
import pandas as pd
import numpy as np
import pickle
import konlpy.tag
import tensorflow as tf
from hanspell import spell_checker
import re
#!pip install transformers
#!pip install konlpy

with open('model/level2_tfidf_vectorizer.pkl', 'rb') as b:
    tfidf = pickle.load(b)

with open('model/level2_estimator.pkl', 'rb') as c:
    load_model = pickle.load(c)

with open('data/level2_dummies.txt', 'rb') as d:
    dummies = pickle.load(d)

okt = konlpy.tag.Okt() # 객체 생성

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '을'
             '를', '으로', '자', '에', '와', '하다', '요', '다', '.', ',']

def to_nan(x):
  if(x == '-'):
    x = ''
  elif(x == '아니오'):
    x = ''
  elif(x == '아뇨'):
    x = ''
  elif(x == '몰라요'):
    x = ''
  elif(x == '모릅니다'):
    x = ''
  elif(x == '모름'):
    x = ''
  elif(x == '아뇨'):
    x = ''
  elif(x == '아뇨'):
    x = ''
  elif(x == '없습니다'):
    x = ''
  elif(x == '없어요'):
    x = ''
  elif(x == '없음'):
    x = ''
  elif(x == '.'):
    x = ''
  return x

def erase_stopwords(text):
  temp_x = okt.morphs(text, stem=True)
  temp_x = [word for word in temp_x if not word in stopwords]
  temp_x = re.findall(r'\w+', str(temp_x))
  temp_x = ' '.join(map(str, temp_x))

  return ' '.join(re.findall(r'\w+', str(temp_x)))

######################
######################

def predict_level(new_data): # Get data as dataframe

  # Change Nan
  new_data = new_data.fillna('-')
  for i in range(len(new_data.columns)):
    new_data[new_data.columns[i]] = new_data.apply(lambda x : to_nan(x[new_data.columns[i]]) , axis = 1 )

  new_data['All'] = new_data['Chief complaint'] + '. ' + new_data['Onset'] + '. ' + new_data['Location']

  # Check spelling
  new_data['All'] = spell_checker.check(new_data['All']).as_dict()['checked']

  # Erase stopwords
  new_data['All'] = new_data.apply(lambda x : erase_stopwords(x['All']) , axis = 1 )

  new_tfidf = tfidf.transform(new_data['All'])

  top_k_result = tf.math.top_k(load_model.predict_proba(new_tfidf), k=3, sorted=True)

  first = top_k_result[1][0][0], top_k_result.values.numpy()[0][0]
  second = top_k_result[1][0][1], top_k_result.values.numpy()[0][1]

  return first, second
