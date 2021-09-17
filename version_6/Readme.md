## Flowchart ###
1. Enter the gender, height, and weight of the user.
2. Receive 'Chief compound', 'Onset', and 'Location' from users and predict major symptoms.
3. Select Key Symptoms
   1. If the difference between top1 and top2 of the predicted major symptoms is less than 10%, the results of top1 and top2 (key symptom names, probability values) are shown.
   2. If the difference between top1 and top2 of the predicted major symptoms is more than 10%, only the results of top1 are shown.
   3. If the user does not think all of the results in 3-1, 3-2 are applicable, press 0 (all or otherwise) (asks questions corresponding to "all" of the list of questions).(20 baseline questions on ver4)
4. Depending on the key symptom values selected by the user, show a list of sheet questions corresponding to questions.xlsx and receive answers. 
(Location Next Questions) + Last Common Question ('Is there anything else unusual?')
5. Pred_disease.py preprocess user inputs and predict disease.
(For females, model ver6_woman_model.h5 is used, and for males, model ver6_men_model.h5 is used without females).)
6. We show the predicted disease top3 results (disease name, probability).

## File Description ##
- ver6_level2_predict.ipynb: Create a model to predict major symptoms (level2) with 'Chief compound', 'Onset', and 'Location'
- ver6_disease_predict(5_17data)-3.ipynb: Create a model that predicts disease based on all symptoms received input

- main.py: The main file, link the three files below and show the results.
- pred_level2.py.py: Load a model for predicting major symptoms, then file for predicting major symptoms of users
- pred_disease.py: files that apply the user's data after loading the symptom-disease prediction model
- Questions_scenarios.py: File organizing the questions in the chatbot

## Additional Data Description ###
- Disease_info2.csv: additional descriptive data of the predicted disease
- questions.xlsx: List of questions not applicable to chatbots, but required for team3 demonstration video
- DB1(2020.5.17)_add_less_5.xlsx: DB1(2020.5.17).xlsx + at_least_10_nan_data.xlsx + 결측치db.xls

## Note ###
- Due to lfs capacity limitation, 'ver6_men_model.h5' and 'ver6_woman_model.h5' have been uploaded to Google Drive. Please download and use the link with model/ver6_models.txt.
- All the data needed to run the ipynb file is in the data folder.

## Installation List ##
- pip install konlpy
- pip install tensorflow
- pip install transformers
- pip install sklearn
- pip install xlrd
- pip install openpyxl
- pip install git+https://github.com/ssut/py-hanspell.git

-------------------------------------------------

## 흐름도 ###
1. 유저의 성별, 키, 몸무게를 입력받는다.
2. 유저의 'Chief complaint', 'Onset', 'Location'을 입력받고 주요 증상을 예측한다.
3. 주요 증상 선택
   1. 예측된 주요 증상의 top1과 top2의 차이가 10% 이하인 경우, top1과 top2의 결과(주요 증상명, 확률값)를 보여준다.
   2. 예측된 주요 증상의 top1과 top2의 차이가 10% 초과인 경우,top1의 결과만 보여준다.
   3. 유저가 만약 3-1, 3-2의 결과 모두 해당이 안된다고 생각한다면 0번(전체 혹은 그 외)을 누른다.(질문목록 중 '전체'에 해당하는 질문들을 묻는다.(ver4의 베이스라인 질문들(20가지))
4. 유저가 선택한 주요 증상 값에 따라 questions.xlsx에 해당되는 시트 질문 목록을 보여주고 답을 받는다. 
   (Location 다음 질문들) + 마지막 공통 질문('다른 특이사항은 없나요?')
5. pred_disease.py에서 유저의 input들을 전처리하고 질병을 예측한다.
   (성별이 여자일 경우, 여성력 질병을 포함한 ver6_women_model.h5 모델을 돌리고 남성인 경우, 여성력 질병이 제외된 ver6_men_model.h5모델을 돌린다.)
6. 예측된 질병 top3결과(질병명, 확률)를 보여준다.

## 파일 설명 ###
- ver6_level2_predict.ipynb: 'Chief complaint', 'Onset', 'Location'으로 주요증상(level2) 예측하는 모델 생성
- ver6_disease_predict(5_17data)-3.ipynb: input받은 모든 증상을 기반으로 질병 예측하는 모델 생성

- main.py: 메인 파일, 아래 세가지 파일을 연결하고 결과들을 보여준다.
- pred_level2.py.py: 주요증상 예측하는 모델을 로드한 뒤, 유저의 주요 증상을 예측하는 파일
- pred_disease.py: 증상-질병 예측 모델을 로드한 뒤, 유저의 데이터를 적용하는 파일
- Questions_scenarios.py: 챗봇의 질문들을 정리한 파일

## 추가 데이터 설명 ###
- Disease_info2.csv: 예측된 질병의 추가 설명 데이터
- questions.xlsx: 챗봇에는 적용되지 않지만, team3의 시연 영상을 위해 필요한 질문 목록
- DB1(2020.5.17)_add_less_5.xlsx: DB1(2020.5.17).xlsx + at_least_10_nan_data.xlsx + 결측치db.xls
 
## 참고 ###
- lfs 용량 제한으로 인해 'ver6_men_model.h5'와 'ver6_women_model.h5'는 구글 드라이브에 업로드 하였습니다. model/ver6_models.txtㅇ 있는 링크를 통해 다운받아 이용해주세요.
- ipynb 파일을 돌리는데 필요하 데이터들은 모두 data폴더에 있습니다.

## 설치 목록 ##
- pip install konlpy
- pip install tensorflow
- pip install transformers
- pip install sklearn
- pip install xlrd
- pip install openpyxl
- pip install git+https://github.com/ssut/py-hanspell.git
