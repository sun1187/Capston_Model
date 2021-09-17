import pandas as pd
import pickle
import numpy as np

with open('data/level2_dummies.txt', 'rb') as d:
    dummies = pickle.load(d)

#disease_info = pd.read_csv('data/Disease_info2.csv')

class Color:
  Red = '\033[31m'
  Green = '\033[32m'
  Yellow = '\033[33m'
  Reset = '\033[0m'
  Cyan = '\033[36m'
  #Blue = '\033[34m'
  #Magenta = '\033[35m'
  #Underline = '\033[4m'

def correct_level2(text):
    if text == '소화불량/만성 복통':
        text = '소화불량_만성복통'
    elif text == '목 통증/허리 통증':
        text = '목 통증_허리 통증'
    elif text == '유방통/유방덩이':
        text = '유방통_유방덩이'
    elif text == '콧물/코막힘':
        text = '콧물_코막힘'
    elif text == '월경이상/월경통':
        text = '월경이상_월경통'
    else:
        text = text
    return text


################## Start
def basic_info():
    print(Color.Cyan + "\n성별은? 남자/여자" + Color.Reset)
    global sex
    sex = input() #쳇봇에서는 선택지

    print(Color.Cyan + "\n나이는? 0s/10s/20s/.../90s/유아/신생아/영아" + Color.Reset)
    global age
    age = input() #챗봇에서는 선택

    print(Color.Cyan + "\n키와 몸무게는?" + Color.Reset)
    global height
    height = input()
    global weight
    weight = input()

    print(Color.Cyan + "\n이제 주요 증상을 알려주세요!" + Color.Reset)
    global chief_complaint
    chief_complaint = input()

    print(Color.Cyan + "\n언제부터 아팠나요?" + Color.Reset)
    global onset
    onset = input()

    print(Color.Cyan + "\n어느 부위가 불편한가요?" + Color.Reset)
    global location
    location = input()

    test_df = {'Chief complaint': chief_complaint,
               'Onset' : onset,
               'Location': location}
    new_data = pd.DataFrame([test_df])

    return new_data

####################### 질문 시나리오 보여주기
def detail_questions(level2):
    test_df = {
      'Height': height,
      'Weight': weight,
      'Age': age,
      'Chief complaint': chief_complaint,
      'Sex': sex,
      'Onset': onset,
      'Location': location, # 여기까지 basic info
      'Duration' : '',
      'Course': '',
      'Experience' : '',
      'Character': '',
      'Associated Sx.': '',
      'Factor': '',
      'Event': '',
      '약물 투약력': '',
      '사회력': '',
      '가족력': '',
      '외상력': '',
      '과거력': '',
      '여성력': '',
    }

    data = pd.DataFrame([test_df])

    level2 = correct_level2(level2)
    questions = pd.read_excel('data/questions.xlsx', sheet_name = level2)
    answer = []

    print(Color.Red + "잘 모르거나 해당 안되는 부분이면 '.' 혹은 '공백'으로 남겨주세요!" + Color.Reset)
    for i in range(7, len(questions['목록'])): # 앞부분은 basic info
      print(Color.Cyan + "\n"+questions['질문'][i] + Color.Reset)
      input_texts = input()
      answer.append(input_texts)

    # 전체 질문에 해당해도 이게 들어가도 왜 오류가 안 뜨는지 확인하기!
    print(Color.Cyan + "\n위 질문 내용 말고도 다른 특이사항은 없었나요?" + Color.Reset)
    input_texts = input()
    answer.append(input_texts)

    data[data.columns[5:len(answer)+5]] = answer

    return data
