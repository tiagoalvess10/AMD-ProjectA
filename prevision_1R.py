import json

"""
Código para prever o diagnóstico de um novo paciente, utilizando o ficheiro com as regras geradas a partir do treino realizado pelo ficheiro onerule.py ou onerule_onetest.py
Pede os valores das variaveis, com exceção da classe, e prevê a classe com base nas regras.
Utiliza a biblioteca json para formatar de JSON para uma string em python para um processamento mais facil
"""



"""
COM DATASET
"""
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
"""

"""
SEM DATASET (HARDCODED)
"""
def create_new_patient():
    new_patient = {}
    variables_list = {
        "age": ["young", "pre-presbyopic", "presbyopic"],
        "prescription": ["myope", "hypermetrope", "astigmatic"],
        "astigmatic": ["yes", "no"],
        "tear_rate": ["normal", "reduced"]
    }

    for variable, values in variables_list.items():
        value = input(f"Enter value for {variable} {values}: ")
        while value not in values:
            print("Invalid value. Please try again.")
            value = input(f"Enter value for {variable} {values}: ")

        new_patient[variable] = value

    return new_patient

def getInformation():
    with open("rules.txt", "r") as f:
        lines = f.readlines()

    best_variable = lines[0].split(":")[1].strip()

    json_str = "".join(lines[2:])
    best_rules = json.loads(json_str)

    return best_variable, best_rules


   
def prevision(new_patient, best_variable, best_rules):
   var_value = new_patient.get(best_variable)
   predicted_class = best_rules.get(var_value)
   print(f"O diagnostico do cliente e: {predicted_class}")
   


response = input("Do you want to predict the diagnosis of a new patient? (yes/no)")
if response.lower() == 'yes':
    #new_patient = create_new_patient(dataset)
    patient_data = create_new_patient()

    best_variable, best_rules = getInformation()

    prevision(patient_data, best_variable, best_rules)
else:
    print("Ending...")