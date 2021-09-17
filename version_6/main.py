#####첫 시작####
from pred_disease import predict_diseases
from pred_level2 import predict_level
from Questions_scenarios import basic_info
from Questions_scenarios import detail_questions
import pandas as pd
import numpy as np
import pickle
#pip install konlpy
#pip install tensorflow
#pip install transformers
#pip install sklearn
#pip install xlrd
#pip install openpyxl
#pip install git+https://github.com/ssut/py-hanspell.git

with open('data/level2_dummies.txt', 'rb') as d:
    dummies = pickle.load(d)

disease_info = pd.read_csv('data/Disease_info2.csv')

class Color:
  Red = '\033[31m'
  Green = '\033[32m'
  Yellow = '\033[33m'
  Reset = '\033[0m'
  Cyan = '\033[36m'
  Magenta = '\033[35m'
  #Blue = '\033[34m'
  #Underline = '\033[4m'

if __name__ == '__main__':
    ################## 1. Start
    print(Color.Yellow + "안녕하세요! Ducktor입니다." + Color.Reset)
    print(Color.Yellow + "진단에 도움될 몇 가지 기본 정보를 입력받겠습니다." + Color.Reset)

    ################### 2. level2 예측
    new_data = basic_info()
    print('\n' + Color.Green + '============질병 예측 범위를 좁히고 있습니다!==========' + Color.Reset)
    #new_data.to_csv('basic_information.csv', index=False)
    first, second = predict_level(new_data)

    if (first[1] - second[1] < 10): # 오차 범위 10%면 top2 질문 시나리오 보여주기
        print('\n' + Color.Green + '27가지 중 아래 2가지 범위의 질병이 예상됩니다.' + Color.Reset)
        print(Color.Green + '해당된다고 생각하면 해당 숫자(1 or 2 )를 선택해주시고,' + Color.Reset)
        print(Color.Green + '해당 안된다고 생각하면 "0"을 선택해주세요.' + Color.Reset)
        print('\n' + Color.Red + dummies[first[0]],':', round(first[1]*100, 2),"%" + Color.Reset)
        print(Color.Red + dummies[second[0]],':', round(second[1]*100, 2),"%" + Color.Reset)
    else:
        print('\n' + Color.Green + '27가지 중 아래 범위의 질병이 예상됩니다.' + Color.Reset)
        print(Color.Green + '해당된다고 생각하면 해당 숫자(1)을 선택해주시고, \n 해당 안된다고 생각하면 "0"을 선택해주세요.' + Color.Reset)
        print('\n' + dummies[first[0]],':', round(first[1]*100, 2),"%")

    receive_number = input()

    ###################### 3. 질문 시나리오 보여주기
    if receive_number == '1':
        data = detail_questions(dummies[first[0]])
    elif receive_number == '2':
        data = detail_questions(dummies[second[0]])
    else:
        data = detail_questions('전체')

    ####################### 4. 질병 예측 결과
    #print(data)

    print(Color.Green + "\n==========확률이 높은 질병 3개를 예측 중입니다.==========" + Color.Reset)
    first, second, third = predict_diseases(data)
    print(Color.Green + "예측 결과(확률이 높은 순으로 나열합니다):" + Color.Reset)

    first_info = disease_info[disease_info['원 질병이름'] == first[0]]
    second_info = disease_info[disease_info['원 질병이름'] == second[0]]
    third_info = disease_info[disease_info['원 질병이름'] == third[0]]

    print(Color.Red + first[0] + Color.Reset)
    print(Color.Red + second[0] + Color.Reset)
    print(Color.Red + third[0] + Color.Reset)

    print('\n' + Color.Green + '질병 설명' + Color.Reset)
    print(Color.Red + '1) ! '+first[0], round(first[1]*100, 2),'%',' !'+ Color.Reset)
    print(Color.Magenta + '동의어:', first_info['동의어'].values[0]+'\n',
          '진료과: ', first_info['진료과'].values[0]+'\n',
          '질병 설명:', first_info['정의'].values[0] + Color.Reset)

    print('\n' + Color.Red + '2) ! '+second[0], round(second[1]*100, 2),'%',' !'+ Color.Reset)
    print(Color.Magenta + '동의어:', second_info['동의어'].values[0]+'\n',
          '진료과: ', second_info['진료과'].values[0]+'\n',
          '질병 설명:', second_info['정의'].values[0] + Color.Reset)

    print('\n' + Color.Red + '3) ! '+third[0], round(third[1]*100, 2),'%',' !'+ Color.Reset)
    print(Color.Magenta + '동의어:', third_info['동의어'].values[0]+'\n',
          '진료과: ', third_info['진료과'].values[0]+'\n',
          '질병 설명:', third_info['정의'].values[0] + Color.Reset)

    print(Color.Red + '!!보다 정확한 진단을 받고 싶다면, 가까운 병원 방문 바랍니다!!' + Color.Reset)
    print(Color.Green + 'Ducktor를 이용해주셔서 감사합니다.' + Color.Reset)

"""
예상 시나리오:
남자
10s
150
50
속이 자주 쓰려요
일주일전
명치 // 실제: 급성 복통

1시간에 한번씩
속이 쓰려요
누워있으면 점점 심해지는 것 같아요
식욕부진, 구토, 메스꺼움
관절염약
술은 1주일에 한번 정도
.
.
.
//실제: 소화성 궤양
"""
