import sys
from u01_util import my_print
import Orange as DM

#_______________________________________________________________________________
# read a "dataset"
# the file name (that can be passed in the command line)
fileName = "./_dataset/d01_lenses.tab"
file_train = "./_dataset/d01_lenses_train.tab"
file_test = "./_dataset/d01_lenses_test.tab"
if len( sys.argv ) > 1: fileName = sys.argv[ 1 ]

try:
    #dataset = DM.data.Table( fileName )
    dataset_train = DM.data.Table(file_train)
    dataset_test = DM.data.Table(file_test)

    tr = DM.classification.TreeLearner()

    classifier = tr(dataset_train)

    class_values = dataset_train.domain.class_var.values

    correct = 0

    for instance in dataset_test:
        predicted_value = class_values[classifier(instance)]
        actual_value = instance.get_class()

        print(f"Predict = {predicted_value}, Actual = {actual_value}, Correct? -> {predicted_value == actual_value}")

        if predicted_value == actual_value:
            correct += 1

    accuracy = correct / len(dataset_test)
    print(f"\nAccuracy: {accuracy*100:.2f}%")

    #printed_tree = classifier.print_tree()      

    #for i in printed_tree.split('\n'):
    #    print(i)

except Exception as e:
   my_print(f"--->>> error - cannot open the file \n{e}")
   exit()


