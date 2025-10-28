import sys
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

#_______________________________________________________________________________
# Lê o dataset
#fileName = "./_dataset/d01_lenses.tab"
fileName = "./_dataset/dataset.tab"

if len(sys.argv) > 1:
    fileName = sys.argv[1]

try:
    df = pd.read_csv(fileName, sep='\t', skiprows=[1,2])

    le_dict = {}
    for col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    loo = LeaveOneOut()
    accuracies = []

    model = DecisionTreeClassifier(criterion="entropy")

    for train_index, test_index in loo.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # Treina o modelo
        model.fit(X_train, y_train)

        # Faz a predição
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        accuracies.append(acc)

    mean_accuracy = sum(accuracies) / len(accuracies)
    print(f"\nAccuracy: {mean_accuracy * 100:.2f}%")

    joblib.dump({'model': model, 'encoders': le_dict}, 'rules_ID3.pkl')

except Exception as e:
    print(f"--->>> error - cannot open the file \n{e}")
    exit()
