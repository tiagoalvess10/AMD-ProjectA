import pandas as pd
import joblib

value = input(f"Do you want to use ID3 or Naive-Bayes classificator?\n1-ID3\n2-Naive-Bayes\n")
if value == "1":
    data = joblib.load('rules_ID3.pkl')
elif value == "2":
    data = joblib.load('rules_NB.pkl')
else:
    print("Invalid option. Please enter 1 or 2.")
    exit()

model = data['model']
le_dict = data['encoders']

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


new_df = pd.DataFrame([new_patient])


for col in new_df.columns:
    new_df[col] = le_dict[col].transform(new_df[col])

# Fazer a predição
pred = model.predict(new_df)

class_encoder = le_dict['lenses']
pred_original = class_encoder.inverse_transform(pred)

print(f"Predicted class for the new patient: {pred_original[0]}")