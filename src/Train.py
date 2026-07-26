from preprocessing import preprocess_data
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
scaled_xtrain, scaled_xtest, y_train, y_test = preprocess_data()

model_lgr = LogisticRegression(max_iter=2000)
model_lgr.fit(scaled_xtrain, y_train)
y_pred = model_lgr.predict(scaled_xtest)
print(model_lgr.score(scaled_xtest,y_test))

print(classification_report(y_test,y_pred))






