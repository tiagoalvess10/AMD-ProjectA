import sys
from u01_util import my_print
import Orange as DM

#_______________________________________________________________________________
# read a "dataset"
# the file name (that can be passed in the command line)
fileName = "./_dataset/d01_lenses.tab"
#fileName = "./_dataset/adult_sample"
if len( sys.argv ) > 1: fileName = sys.argv[ 1 ]

try:
    dataset = DM.data.Table( fileName )

    nb = DM.classification.NaiveBayesLearner()

    classifier = nb(dataset)

    print(classifier(dataset[0:3], True))

except Exception as e:
   my_print(f"--->>> error - cannot open the file: {fileName}\n{e}")
   exit()


