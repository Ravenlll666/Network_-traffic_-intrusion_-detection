import Evaluate
from preprocessing import preprocess_data
import pandas as pd
import matplotlib.pyplot as plt          
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV 
from Evaluate import evaluate_model
import joblib
scaled_xtrain, scaled_xtest, y_train, y_test,scaler,One_hot_encoding,label_encoder = preprocess_data()




model_lgr = LogisticRegression(max_iter=2000,random_state=42)
model_lgr.fit(scaled_xtrain, y_train)
y_pred_log = model_lgr.predict(scaled_xtest)
accuracy_logr=model_lgr.score(scaled_xtest,y_test)
Evaluate
evaluate_model(
    y_test,
    y_pred_log,
    "Logistic Regression"
)



#Decision Tree 
dtc = DecisionTreeClassifier(criterion='gini',random_state=42 )
dtc.fit(scaled_xtrain,y_train )
y_pred_dtc = dtc.predict(scaled_xtest)
accuracy_dtc=dtc.score(scaled_xtest,y_test)
#Evaluate
evaluate_model(
    y_test,
    y_pred_dtc,
    "Decision Tree"
)

#Random Forest 
rfc = RandomForestClassifier(
    n_estimators=100,
    min_samples_split=5,
    min_samples_leaf=1,
    max_features='sqrt',
    max_depth=20,
    random_state=42
)

rfc.fit(scaled_xtrain, y_train)

y_pred_rfc = rfc.predict(scaled_xtest)

accuracy_rfc = rfc.score(scaled_xtest, y_test)

evaluate_model(
    y_test,
    y_pred_rfc,
    "Optimized Random Forest"
)

#SVM
# svm = SVC(kernel='rbf',random_state=42)
# svm.fit(scaled_xtrain, y_train)
# y_pred_svm = svm.predict(scaled_xtest)
# accuracy_svm = svm.score(scaled_xtest, y_test)


# evaluate_model(
#     y_test,
#     y_pred_svm,
#     "SVC"
# )
print("%90")
# XGBoost
from xgboost import XGBClassifier

xgb = XGBClassifier(
    subsample=1.0,
    n_estimators=300,
    max_depth=7,
    learning_rate=0.2,
    colsample_bytree=1.0,
    random_state=42
)

xgb.fit(scaled_xtrain, y_train)

y_pred_xgb = xgb.predict(scaled_xtest)

accuracy_xgb = xgb.score(scaled_xtest, y_test)

evaluate_model(
    y_test,
    y_pred_xgb,
    "Optimized XGBoost"
)
import joblib

joblib.dump(xgb, "model/xgb_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
joblib.dump(One_hot_encoding, "model/encoder.pkl")
joblib.dump(label_encoder,'model/label_encoder.pkl')

print("Model Saved Successfully")