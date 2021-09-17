# -*- coding: utf-8 -*-
"""Ver6_disease_predict(5.17data).ipynb"""
import pandas as pd
import numpy as np
import tensorflow as tf
from transformers import FunnelTokenizerFast
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from hanspell import spell_checker
import pickle
import konlpy.tag
import re

with open('model/ver6_men_tokenizer.pickle', 'rb') as handle:
    m_tokenizer = pickle.load(handle)
with open('model/ver6_women_tokenizer.pickle', 'rb') as handle:
    w_tokenizer = pickle.load(handle)

m_loaded_model = load_model('model/ver6_men_model.h5')
w_loaded_model = load_model('model/ver6_women_model.h5')

with open("data/ver6_men_diseases.txt", "rb") as fp:
    m_disease_codes = pickle.load(fp)
with open("data/ver6_women_diseases.txt", "rb") as fp:
    w_disease_codes = pickle.load(fp)

#disease_info = pd.read_csv('data/Disease_info2.csv')

okt = konlpy.tag.Okt() # 객체 생성

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
  elif(x == '없습니다'):
    x = ''
  elif(x == '없어요'):
    x = ''
  elif(x == '없음'):
    x = ''
  elif(x == '.'):
    x = ''
  return x

def NRS_to_text(text):
  a = re.findall('NRS.*?점', text) #NRS 5점
  if len(a) == 0:
    a = re.findall('NRS.*?\d~\d', text) #NRS 4~6 / NRS : 4~6
  if len(a) == 0:
    a = re.findall('NRS.*?\d', text) #NRS: 5
  try:
    t = re.findall('[0-9]+', a[0])
    if (len(t) == 2):
      score = (int(t[0])+int(t[1]))/ 2
    else:
      score = int(t[0])
    if score >= 7:
      to_text = '심함'
    elif score >= 4:
      to_text = '중간'
    else:
      to_text = '약함'
    text = text.replace(a[0], to_text)
  except:
    pass
  return text

def spelling_check(text):
  result = spell_checker.check(text)
  return result.as_dict()['checked']

def define_obesity(x):
  if x < 0:
    return '알 수 없음'
  elif x < 20.0:
    return '저체중'
  elif x <= 24.0:
    return '정상'
  elif x <= 29.0:
    return '과체중'
  else:
    return '비만'

def only_letters_num(x):
  return ' '.join(re.findall(r'\w+', str(x)))

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '을'
             '를', '으로', '자', '에', '와', '하다', '요', '다', '.', ',']

def erase_stopwords(text):
  temp_x = okt.morphs(text, stem=True)
  temp_x = [word for word in temp_x if not word in stopwords]
  temp_x = re.findall(r'\w+', str(temp_x))
  temp_x = ' '.join(map(str, temp_x))
  return ' '.join(re.findall(r'\w+', str(temp_x)))

####################
m_max_len = 162
w_max_len = 162
#m_max_words = 1600, w_VOCAB_SIZE = 1800
#EMBEDDING_DIM = 1000
######################

def predict_diseases(data): # Get data as dataframe

  # Change Nan to blank text
  data = data.fillna('-')

  # Fill blank text
  for i in range(len(data.columns)):
    data[data.columns[i]] = data.apply(lambda x : to_nan(x[data.columns[i]]) , axis = 1 )

  # Define obesity by calculating BMI with Height and Weight
  data['Height'] = data['Height'].replace('', '0')
  data['Weight'] = data['Weight'].replace('', '0')

  data['Height'] = data['Height'].astype('int')
  data['Weight'] = data['Weight'].astype('int')

  data['BMI'] = data['Weight'] / (data['Height']/100)**2
  data['BMI'].fillna(-1, inplace=True)
  data['Obesity'] = define_obesity(data['BMI'].values)

  # Change Age to Groups of AgeX(-> Since we are going to receive their age as a group_format)
  data['Age'] = data['Age'].astype(str)

  # Make a sentence
  data['All'] = (data['Chief complaint'].values +'. '+ data['Age'].values + '. '+
                  data['Onset'].values + '. '+ data['Location'].values + '. ' +
                  data['Sex'].values + '. '+
                  data['Duration'].values + '. ' + data['Course'].values + '. ' +
                  data['Experience'].values + '. ' + data['Character'].values + '. ' +
                  data['Associated Sx.'].values+'. '+ data['Factor'].values + '. ' +
                  data['Event'].values + '. ' + data['약물 투약력'].values + '. ' +
                  data['사회력'].values + '. ' + data['가족력'].values + '. ' +
                  data['외상력'].values + '. ' + data['과거력'].values + '. ' +
                  data['여성력'].values + '. ' + data['Obesity'].values)

  # Change NRS to text
  data['All'] = NRS_to_text(data['All'].values[0])

  # Spelling Check
  data['All'] = spelling_check(data['All'].values[0])

  # Erase stopwords using konlpy
  data['All'] = erase_stopwords(data['All'].values[0])

  #data.to_csv('all_data.csv', index=False)
  data['All'] = only_letters_num(data['All'].values)
  document_bert_data = ["[CLS] " + str(s) + " [SEP]" for s in data['All'].values]

  # Tokenizer: LMKor_funnel: https://github.com/kiyoungkim1/LMkor
  tokenizer_funnel = FunnelTokenizerFast.from_pretrained("kykim/funnel-kor-base")
  if data['Sex'].values =='남자':
      #print('성별이 남자일 때')
      ko_tokenized_texts_data = [tokenizer_funnel.tokenize(s) for s in document_bert_data]
      data_sequence = m_tokenizer.texts_to_sequences(ko_tokenized_texts_data)
      data_sequence = pad_sequences(data_sequence, maxlen = m_max_len).reshape(1,-1)
      y_prob = m_loaded_model.predict(data_sequence)

      top_k_result = tf.math.top_k(y_prob, k=3, sorted=True)

      first_name = m_disease_codes[top_k_result[1][0][0]]
      second_name = m_disease_codes[top_k_result[1][0][1]]
      third_name = m_disease_codes[top_k_result[1][0][2]]

      first_proba = top_k_result.values.numpy()[0][0]
      second_proba = top_k_result.values.numpy()[0][1]
      third_proba = top_k_result.values.numpy()[0][2]

      first_disease = first_name, first_proba
      second_disease = second_name, second_proba
      third_disease = third_name, third_proba

  else: # 성별이 '여자' 일 때:
      #print('성별이 여자일 때')
      ko_tokenized_texts_data = [tokenizer_funnel.tokenize(s) for s in document_bert_data]
      data_sequence = w_tokenizer.texts_to_sequences(ko_tokenized_texts_data)
      data_sequence = pad_sequences(data_sequence, maxlen = w_max_len).reshape(1,-1)
      y_prob = w_loaded_model.predict(data_sequence)

      top_k_result = tf.math.top_k(y_prob, k=3, sorted=True)

      first_name = w_disease_codes[top_k_result[1][0][0]]
      second_name = w_disease_codes[top_k_result[1][0][1]]
      third_name = w_disease_codes[top_k_result[1][0][2]]

      first_proba = top_k_result.values.numpy()[0][0]
      second_proba = top_k_result.values.numpy()[0][1]
      third_proba = top_k_result.values.numpy()[0][2]

      first_disease = first_name, first_proba
      second_disease = second_name, second_proba
      third_disease = third_name, third_proba

  return first_disease, second_disease, third_disease
