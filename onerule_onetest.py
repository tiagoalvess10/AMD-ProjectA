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
import json
from collections import Counter

"""
Algorithm: One Rule (OneR) manual implementation

Ver a descrição do ficheiro onerule.py

Este código realiza o mesmo processamento do onerule.py, com a diferenca dos datasets utilizados e do numero de vezes que o algoritmo treina e testa.

Em vez de ter um dataset de treino e teste predefinido, o algoritmo treina com N-1 instancias de um dataset e testa com a instancia que ficou de fora.
Após isso, realiza o mesmo processo mas com outra instancia de fora.
Posto isto, este codigo realizei N treinos e testes, sendo N o tamanho do dataset e utilizando sempre para teste uma instancia diferente.

Este processamento é denominado Leave One Out.

Quando acaba um processamento guarda num array as rules, a melhor variavel e a previsão, para que, quando realizar os N processamentos, recolha a informação
da variavel que foi mais vezes classificada como a melhor, assim como as rules, e faz a media das accuracies, ficando com a accuracy media que é a que será analisada.
"""
def one_rule(dataset):
   variable_list = dataset.domain.attributes       # attributes para que exclua a class, se fosse varibles incluiria a class
   class_var = dataset.domain.class_var            # a variável classe
   N = len(dataset)                                # tamanho do dataset

   best_accuracy = 0.0                             # variavel para guardar a melhor accuracy, que é utilizada no final 
   best_variable = None                            # variavel para guardar a melhor variável, que é utilizada no final  
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

      c_rules = {}
      for value in variable.values:
         max_count = 0
         best_class = None
         for class_value in class_var.values:
            if best_class is None:                 # primeira vez
               best_class = class_value
               max_count = frequency[value, class_value]
            else:
               count = frequency[value, class_value]
               if count > max_count:
                  max_count = count
                  best_class = class_value

         c_rules[value] = best_class
            

      correctPredict = 0
      for data in dataset:
         var_value = str(data[variable])
         predicted_class = c_rules.get(var_value)
         actual_class = str(data[class_var])
         if predicted_class == actual_class:
            correctPredict += 1

      accuracy = correctPredict / N
      #print(f"Variable: {variable.name}, Accuracy: {accuracy:.2f}")

      if accuracy > best_accuracy:
         best_accuracy = accuracy
         best_variable = variable
         best_rules = c_rules
         
      
   #print("\nBest variable:", best_variable.name)
   #print("Accuracy:", f"{best_accuracy:.2f}")
   #print("Rules:", best_rules)

   return best_variable, best_rules

def test(best_variable, best_rules, dataset):

   correct = 0
   for instance in dataset:
      var_value = str(instance[best_variable])
      predicted_value = best_rules.get(var_value)
      actual_value = str(instance[dataset.domain.class_var])
      #print(f"Predict = {predicted_value}, Actual = {actual_value}, Correct? -> {predicted_value == actual_value}")

      if predicted_value == actual_value:
         correct += 1

   accuracy = correct / len(dataset)
   #print(f"\nAccuracy: {accuracy*100:.2f}%")

   return accuracy

def leave_one_out(dataset):
   N = len(dataset)
   accuracies = []
   bestVariables = []
   bestRules = []

   for i in range(N):

      train_indices = [j for j in range(N) if j != i]
      train_dataset = dataset[train_indices]
      print("Train dataset")
      #print()
      #print(train_dataset)
      
      test_dataset = dataset[i:i+1]
      #print("Teste dataset")
      #print()
      #print(test_dataset)

      #print()
      #print("end")
      #print()

      best_variable, best_rules = one_rule(train_dataset)

      accuracy = test(best_variable, best_rules, test_dataset)

      accuracies.append(accuracy)

      bestVariables.append(best_variable.name)
      bestRules.append(best_rules)

      #print(f"Iteracao {i+1}/{N} -> Accuracy: {accuracy:.2f}")

   mean_accuracy = sum(accuracies) / N
   variable_counter = Counter(bestVariables)
   most_common_variable = variable_counter.most_common(1)[0][0]

   index = bestVariables.index(most_common_variable)
   most_common_rules = bestRules[index]

   return mean_accuracy, most_common_variable, most_common_rules

#_______________________________________________________________________________
# read a "dataset"
# the file name (that can be passed in the command line)
fileName = "./_dataset/d01_lenses.tab"

if len( sys.argv ) > 1: fileName = sys.argv[ 1 ]

try:
   dataset = DM.data.Table( fileName )
   #print(dataset)
   #print("\n")

   mean_accuracy, variable, rules = leave_one_out(dataset)

   print(f"Mean Accuracy: {mean_accuracy*100:.2f}%")
   #print(f"Most Frequent Best Variable: {variable}")
   #print("Rules:")
   for value, class_value in rules.items():
      print(f"  {value} -> {class_value}")

   with open("rules.txt","w") as file:
        file.write("best variable: ")
        file.write(variable)
        file.write("\n")
        file.write("Rules:\n")
        json.dump(rules, file, indent=4)
    
except Exception as e:
    my_print(f"--->>> error - cannot open the file \n{e}")
    exit()

