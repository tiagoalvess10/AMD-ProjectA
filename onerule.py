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

"""
Algorithm: One Rule (OneR) manual implementation
Recebe, como parâmetro, um dataset

Primeiro percorre todas as variáveis (atributos) do dataset e, para cada varivel, constroi um dicionrio de frequncias,
para contar as ocorrências de cada valor da varivel em relação a cada valor da classe.
No inicio, esse dicionário é inicializado com 0 para todas as combinações possíveis de valores da varivel e da classe.

Depois, percorre todas as instâncias do dataset, atualizando o dicionário de frequências com as contagens reais.

Em seguida, para cada valor da varivel, determina a classe mais frequente associada a esse valor, construindo assim as regras de classificação.

Após isso, conta o numero de previsões corretas feitas pelas regras construídas, utilizando o correctPredict.

Após contar em quantos casos a varivel previu corretamente a classe, calcula a accuracy, isto é, 
a proporção de previsões corretas em relação ao número total de instâncias.

Por fim, compara a accuracy obtida com a melhor accuracy encontrada até o momento.
Se a accuracy atual for maior, atualiza a melhor accuracy e armazena a varivel correspondente.
Assim, teremos a varivel que melhor classifica o dataset com base na accuracy.
Por fim, escreve a melhor variavel e as regras de classificacao num ficheiro para poderem ser posteriormente utilizadas em previsoes

Depois de treinar com um dataset, testa com outro dataset e apresenta a accuracy
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
      print(f"Variable: {variable.name}, Accuracy: {accuracy:.2f}")

      if accuracy > best_accuracy:
         best_accuracy = accuracy
         best_variable = variable
         best_rules = c_rules
         
      
   print("\nBest variable:", best_variable.name)
   print("Accuracy:", f"{best_accuracy:.2f}")
   print("Rules:", best_rules)

   return best_variable, best_rules

def test(best_variable, best_rules, dataset):

   correct = 0
   for instance in dataset:
      var_value = str(instance[best_variable])
      predicted_value = best_rules.get(var_value)
      actual_value = str(instance[dataset.domain.class_var])
      print(f"Predict = {predicted_value}, Actual = {actual_value}, Correct? -> {predicted_value == actual_value}")

      if predicted_value == actual_value:
         correct += 1

   accuracy = correct / len(dataset)
   print(f"\nAccuracy: {accuracy*100:.2f}%")
   

#_______________________________________________________________________________
# read a "dataset"
# the file name (that can be passed in the command line)
fileName = "./_dataset/d01_lenses.tab"
file_train = "./_dataset/d01_lenses_train.tab"
file_test = "./_dataset/d01_lenses_test.tab"

if len( sys.argv ) > 1: fileName = sys.argv[ 1 ]

try:
   #dataset = DM.data.Table( file )
   #print(dataset)
   #print("\n")

   dataset_train = DM.data.Table(file_train)
   dataset_test = DM.data.Table(file_test)


   print("############### TREINO ################")
   best_variable, best_rules = one_rule(dataset_train)

   print("\n############### TESTES ################")
   test(best_variable, best_rules, dataset_test)

   with open("rules.txt","w") as file:
      file.write("best variable: ")
      file.write(best_variable.name)
      file.write("\n")
      file.write("Rules:\n")
      json.dump(best_rules, file, indent=4)
   
except Exception as e:
   my_print(f"--->>> error - cannot open the file \n{e}")
   exit()

