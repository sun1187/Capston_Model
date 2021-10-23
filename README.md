The latest model is in folder 'version_6'.

<img width="828" alt="스크린샷 2021-10-23 오후 11 17 54" src="https://user-images.githubusercontent.com/70509258/138560537-95a1d486-4c11-4321-b275-fb0b9d83e94e.png">

# Motivation for Development:
There are times when there is no hospital in the area near the residence, it is difficult for the patient to visit the hospital due to the burden of medical expenses, or when they want to receive medical treatment quickly and conveniently due to the burden of visiting in person. Through this, We thought it would be nice to have a service that provides simple non-face-to-face diagnosis through chatbots. Accordingly, based on the theme of developing a chatbot customized and symptom-disease prediction algorithm, our team worked on a project to develop an algorithm that can predict diseases through a machine learning model when patients enter information about symptoms.

# User's Point of View:
The approximate workflow is as follows. Based on the basic information entered by the user, major symptoms are predicted, and additional symptom information is input through questions corresponding to the predicted major symptoms to predict and show the three most likely diseases.

<img width="780" alt="스크린샷 2021-10-23 오후 11 56 11" src="https://user-images.githubusercontent.com/70509258/138561444-b9c8bd8f-3fff-4f35-8ac2-1bdf41c2e4fc.png">

# Results of Major Symptom Prediction Model:
|Model|Test Acc|Test F1-Score|
|:---:|:---:|:---:|
|Multinomial Naive Bayes|0.92|0.92|
|Support Vector Machine|0.95|0.94|
|<span style="color:red">Random Forest Classifier</span>|<span style="color:red">0.96</span>|<span style="color:red">0.96</span>|
|Decision Tree Classifier|0.94|0.95|

# Structure of Disease Predicting Models:
The structure model is as follows. Reflects the context by adding lstm, applies three different filters in cnn, goes through dropout and dense layers to prevent maxpooling 1d, concatenate and multiple overfitting, and predicts the disease with a softmax activation function. In addition, Model 1 was slightly lower than Model 2, so the part that connected lstm and cnn was added to supplement it.
27 major sypmtoms and 
## Evaluation
|Model|Test Acc|Test F1-Score|Top3 Hitrate|
|:---:|:---:|:---:|:---:|
|Model 1 (For Male)|0.82|0.88|0.91|
|Model 2 (For Female)|0.80|0.87|0.91|

# Result
<img width="747" alt="스크린샷 2021-10-23 오후 11 25 10" src="https://user-images.githubusercontent.com/70509258/138560819-7ac2fbb4-1f5b-4a9b-bb85-b82699890909.png">
<img width="412" alt="스크린샷 2021-10-23 오후 11 25 06" src="https://user-images.githubusercontent.com/70509258/138560820-d1a743ce-307e-441a-871f-a93a8c3d213d.png">

## LICENCE
The MIT License (MIT) Copyright (c) 2021 이재훈, 김은선, 이현진, 정정민, Chomedicine
