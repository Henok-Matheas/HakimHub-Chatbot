import sys
import os
import json

current_dir = os.path.dirname(__file__)

sys.path.append(os.path.join(current_dir, "../utils"))
import file_handlers
sys.path.append(os.path.join(current_dir, "../"))
import chat

def benchmark():
    specs_with_symptoms_file = os.path.join(current_dir,"./test_data/specializations-with-symptoms.json")
    # specs_with_symptoms_file = os.path.join(current_dir,"./test_data/specializations-with-symptoms-kaggle.json")
    specs_with_symptoms = file_handlers.load_json(specs_with_symptoms_file)
    length = 0
    absolute_match = 0
    match = 0

    # for specialization in specs_with_symptoms:
    #     symptoms = specs_with_symptoms[specialization]

    for spec_with_symptoms in specs_with_symptoms:
        specialization = spec_with_symptoms["specialization"]
        total_symptoms = spec_with_symptoms["symptoms"]

        for symptoms in total_symptoms:
            length += 1
            conversation = chat.load_new_chat()

            message = f""""I have a {" ".join(symptoms)}"""

            output = conversation.predict(input = message)
            output = json.loads(output)

            predicted_specialization = output["specialization"]
            message = output["message"]

            if predicted_specialization.lower() == specialization.lower():
                absolute_match += 1
                match += 1
            elif not predicted_specialization:
                match += 1
            else:
                print(message)

    print(f"""
          The total number of symptoms: {length}
          The chatbot has two types of accuracy:
          1. absolute accuracy which checks for exact match and doesn't consider the ones where the chatbot wants more data: {(absolute_match / length) * 100}%
          2. match which considers for the cases where the chatbot wants more data: {(match / length) * 100}%
          """)


benchmark()
