import sys
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

"""
Este codigo realiza o algoritmo de classificação ID3, utilizando a biblioteca sklearn, em vez do orange framework uma vez que achou-se que neste caso 
seria mais simples, uma vez que existe muita documentação acerca desta biblioteca e ficava mais simples de implementar a técnica de validação Leave One Out que seria
uma melhor abordagem do que repartir o dataset em treino e teste apenas uma vez, como no código ID3ive_Bayes.py 

Assim sendo, em vez de existir um dataset de treino e teste predefinido, o algoritmo treina com N-1 instancias de um dataset e testa com a instancia que ficou de fora.
Após isso, realiza o mesmo processo mas com outra instancia de fora.
Posto isto, este codigo realiza N treinos e testes, sendo N o tamanho do dataset e utilizando sempre para teste uma instancia diferente.

Após realizar todos os treunos e testes, apresenta a accuracy para vermos o desempenho do classificador.

Por fim, treina com o dataset completo e guarda o modelo num ficheiro rules_ID3.pkl, que é um tipo de ficheiro binários utilizado em Python para guardar objetos,
que é exatamente o que queremos ao guardar o modelo. Este tipo de ficheiro é muito utilizado para guardar modelos de machine learning treinados, como é o caso.
Algumas das vantagens são: a rapidez, a simplicidade, a versatilidade e a integração.

Utiliza a biblioteca joblib para guardar os dados no ficheiro
"""

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

    model.fit(X, y)

    joblib.dump({'model': model, 'encoders': le_dict}, 'rules_ID3.pkl')

except Exception as e:
    print(f"--->>> error - cannot open the file \n{e}")
    exit()
