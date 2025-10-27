import sys
from u01_util import my_print
import Orange as DM

from sklearn.model_selection import LeaveOneOut
"""
Este codigo realiza o algoritmo de classificação ID3 presente no orange framework. Podia ser utilizado o do scikit-learn, mas deu-se preferência a esta biblioteca
uma vez que estamos a trabalhar com o orange.

Treina e testa com datasets diferentes e apresenta a accuracy do algoritmo
"""

#_______________________________________________________________________________
# read a "dataset"
# the file name (that can be passed in the command line)
#fileName = "./_dataset/d01_lenses.tab"
fileName = "./_dataset/dataset.tab"
#file_train = "./_dataset/d01_lenses_train.tab"
#file_test = "./_dataset/d01_lenses_test.tab"
#file_train = "./_dataset/dataset_train.tab"
#file_test = "./_dataset/dataset_test.tab"

if len( sys.argv ) > 1: fileName = sys.argv[ 1 ]

try:
    dataset = DM.data.Table( fileName )
    
    N = len(dataset)
    accuracies = []

    loo = LeaveOneOut()
    indices = list(range(N))
    iteration = 1

    tr = DM.classification.TreeLearner()

    for train_index, test_index in loo.split(indices):

        train_dataset = dataset[train_index]
        test_dataset = dataset[test_index]
        
        """
        print("Train dataset")
        print()
        print(train_dataset)
        print("Teste dataset")
        print()
        print(test_dataset)
        print()
        print("end")
        print()
        """
        

        classifier = tr(train_dataset)

        class_values = train_dataset.domain.class_var.values

        correct = 0

        for instance in test_dataset:
            predicted_value = class_values[classifier(instance)]
            actual_value = instance.get_class()

            #print(f"Predict = {predicted_value}, Actual = {actual_value}, Correct? -> {predicted_value == actual_value}")

            if predicted_value == actual_value:
                correct += 1

            accuracy = correct / len(test_dataset)
            #print(f"\nAccuracy: {accuracy*100:.2f}%")
      
        accuracies.append(accuracy)

        #print(f"Iteracao {iteration}/{N} -> Accuracy: {(accuracy*100):.2f}%")
        #iteration = iteration + 1

    mean_accuracy = sum(accuracies) / N

    print(f"\nAccuracy: {mean_accuracy*100:.2f}%")

except Exception as e:
   my_print(f"--->>> error - cannot open the file \n{e}")
   exit()


