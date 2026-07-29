from preprocessing import preprocess_data
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import RandomForestClassifier
from Evaluate import evaluate_model



scaled_xtrain, scaled_xtest, y_train, y_test = preprocess_data()

model_lgr = LogisticRegression(max_iter=2000)
model_lgr.fit(scaled_xtrain, y_train)
y_pred_log = model_lgr.predict(scaled_xtest)
accuracy_logr=model_lgr.score(scaled_xtest,y_test)
#Evaluate
evaluate_model(
    y_test,
    y_pred_log,
    "Logistic Regression"
)



#Decision Tree 
dtc = DecisionTreeClassifier(criterion='gini' )
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
rfc = RandomForestClassifier()
rfc.fit(scaled_xtrain,y_train )
y_pred_rfc = rfc.predict(scaled_xtest)
accuracy_rfc=rfc.score(scaled_xtest,y_test)

evaluate_model(
    y_test,
    y_pred_rfc,
    "Random Forest"
)


