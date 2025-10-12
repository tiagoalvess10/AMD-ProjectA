# to use accented characters in the code
# -*- coding: cp1252 -*-
# ===============================
# author: Paulo Trigo Silva (PTS)
# v08 (Python39, Orange3)
# ===============================


#__________________________________________
# Orange Documentation:
# http://docs.orange.biolab.si
#
# Orange Reference Manual:
# http://docs.orange.biolab.si/3/data-mining-library/#reference
#
# Tutorial:
# http://docs.orange.biolab.si/3/data-mining-library/#tutorial
#
# details about data (attribute+class) characterization:
# http://docs.orange.biolab.si/3/data-mining-library/tutorial/data.html#data-input
#__________________________________________

#_______________________________________________________________________________
# Modules to Evaluate
import sys
from u01_util import my_print
import Orange as DM

"""
Algorithm: One Rule (OneR) manual implementation
"""
def one_rule(dataset):
   variable_list = dataset.domain.attributes 
   class_var = dataset.domain.class_var 
   N = len(dataset)

   best_accuracy = 0.0
   best_variable = None
   best_rules = None

   for variable in variable_list:
      frequency = {}
      for value in variable.values:
         for class_value in class_var.values:
            frequency[value, class_value] = 0

      for data in dataset:
         var_value = str(data[variable])
         class_value = str(data[class_var])
         frequency[var_value, class_value] += 1

      rules = {}
      for value in variable.values:
         max_count = 0
         best_class = None
         for class_value in class_var.values:
            if best_class is None:
               best_class = class_value
            else:
               count = frequency[value, class_value]
               if count > max_count:
                  max_count = count
                  best_class = class_value

         rules[value] = best_class
            

      n_predictions = 0
      for data in dataset:
         var_value = str(data[variable])
         predicted_class = rules.get(var_value)
         actual_class = str(data[class_var])
         if predicted_class == actual_class:
            n_predictions += 1

      accuracy = n_predictions / N
      print(f"Variable: {variable.name}, Accuracy: {accuracy:.2f}")

      if accuracy > best_accuracy:
         best_accuracy = accuracy
         best_variable = variable
         best_rules = rules
      
   print("\nBest variable:", best_variable.name)
   print("Accuracy:", f"{best_accuracy:.2f}")
   print("Rules:", best_rules)

#_______________________________________________________________________________
# read a "dataset"
# the file name (that can be passed in the command line)
fileName = "./_dataset/d01_lenses.tab"
#fileName = "./_dataset/adult_sample"
if len( sys.argv ) > 1: fileName = sys.argv[ 1 ]

try:
   dataset = DM.data.Table( fileName )
   one_rule(dataset)
   #print( dataset )
   #print (dataset.domain)
   #print (dataset.domain.variables)
   #print (dataset.domain.attributes)
   #print("\n\n\n\n\n\n\n\n")
   #print (dataset.domain.class_var)
   #print (dir(dataset.domain.class_var))
   
except Exception as e:
   my_print(f"--->>> error - cannot open the file: {fileName}\n{e}")
   exit()


"""
#_______________________________________________________________________________
# variables: name (type = discrete | continuous): [value1, value2, ...]
# variables, in Orange, refer to features or class
# cf., http://docs.orange.biolab.si/3/data-mining-library/tutorial/data.html#exploration-of-the-data-domain
variable_list = dataset.domain.variables
variable_list = dataset.domain.attributes

my_print( aStr = ">> %d Variables (attributes+class) <<" % len( variable_list ) )
print( ">> name (type): (value1, value2, ...) <<" )

nDisc=0; nCont=0; nStr=0
for variable in variable_list:
   print( ":: %s %s" % ( variable.name, variable.TYPE_HEADERS ), end="" ),
   if variable.is_discrete:
      print( ": {0} ".format( variable.values ) )
      #print( variable.values )
      nDisc += 1
   elif variable.is_continuous:
      print()
      nCont += 1
   else:
      nStr += 1
my_print( ">> Types: %d discrete, %d continuous <<" % ( nDisc, nCont ) )



#_______________________________________________________________________________
# Class: name (type = discrete | continuous): <value1, value2, ...>
the_class = dataset.domain.class_var
my_print( ">> Class <<" )
print( ":: %s %s: %s " % ( the_class.name,
                           the_class.TYPE_HEADERS,
                           the_class.values ) )



#_______________________________________________________________________________
# First N Instances
N = 8
my_print( "First %d instances:" % N )
for i in range( N ): print( dataset[ i ] )

"""
