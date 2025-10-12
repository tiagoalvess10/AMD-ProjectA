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
Assim, teremos a varivel que melhor classifica o dataset com base na accuracy. Essas informações são apresentadas no final.
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

"""
Tendo
"""
def create_new_patient(dataset):
   new_patient = {}
   variable_list = dataset.domain.attributes
   for variable in variable_list:
      value = input(f"Enter value for {variable.name} {variable.values}: ")
      while value not in variable.values:
         print("Invalid value. Please try again.")
         value = input(f"Enter value for {variable.name} {variable.values}: ")
      new_patient[variable.name] = value

   return new_patient

   
def prevision(new_patient, best_variable, best_rules):
   var_value = new_patient.get(best_variable.name)
   predicted_class = best_rules.get(var_value)
   print(f"O diagnostico do cliente e: {predicted_class}")
   
#_______________________________________________________________________________
# read a "dataset"
# the file name (that can be passed in the command line)
fileName = "./_dataset/d01_lenses.tab"
#fileName = "./_dataset/adult_sample"
if len( sys.argv ) > 1: fileName = sys.argv[ 1 ]

try:
   dataset = DM.data.Table( fileName )
   print(dataset)
   print("\n")
   best_variable, best_rules = one_rule(dataset)
   print("\n")
   response = input("Deseja prever o diagnostico de um novo paciente? (yes/no)")
   if response.lower() == 'yes':
      new_patient = create_new_patient(dataset)
      prevision(new_patient, best_variable, best_rules)
   else:
      print("Ending...")

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
