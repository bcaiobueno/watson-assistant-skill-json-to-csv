import json
import csv
import re

# --------------------------------------------------------------
# --------------------- HOW TO USE -----------------------------
# --------------------------------------------------------------
# Download the output JSON file from Watson Assistant Workspace
# Paste the downloaded file into the root of this project
# Change the name of the file on line 20 and just RUN !!!!
# --------------------------------------------------------------
# --------------------------------------------------------------

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Reads the JSON file and convert to dictionary ---------
with open('YOUR-FILE-NAME.json') as json_file:
    data = json.load(json_file)

# --------------------------------------------------------
# Creates a csv file with all the intents and the examples
# --------------------------------------------------------
intents_and_examples = ['Intent', 'Example'] # CSV Header
with open('intents_and_examples.csv', mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, intents_and_examples)
    writer.writeheader()
    for item in data['intents']:
        intent = item['intent']
        print('Intent: '+ str(intent))
        for example in item['examples']:
            examples = example['text']
            print('Examples: ' + str(examples))
            writer.writerow({'Intent': intent, 'Example': examples})

# --------------------------------------------------------
# Creates a csv file with all the entities and synonyms
# --------------------------------------------------------
entities = ['Entity_Name', 'Value', 'Synonyms'] # CSV Header
with open('entities_and_synonyms.csv', mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, entities)
    writer.writeheader()
    for item in data['entities']:
        entity = item['entity']
        print('Entity: '+ str(entity))
        for value in item['values']:
            values = value['value']
            print(values)
            synonyms = ''
            for synonym in value['synonyms']:
                synonyms = synonyms + '/' + synonym
                print('Synonyms: '+ str(synonyms))
            writer.writerow({'Entity_Name': entity, 'Value': values, 'Synonyms': synonyms})


# -----------------------------------------------------------
# Creates a csv file with all the answers and intents related
# -----------------------------------------------------------
answers_header = ['Condition', 'Output'] # CSV Header
with open('conditions_and_outputs.csv', mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, answers_header)
    writer.writeheader()

    for node in data['dialog_nodes']:
        try:
            condition = node['conditions'] if 'conditions' in node and 'conditions' is not None else None
            output = node['output']['text']['values'][0] if 'output' in node and 'output' is not None else None
            clean_output = cleanhtml(output)
            print('Condition: '+ str(condition))
            print('Output: ' + str(clean_output))
            writer.writerow({'Condition': condition, 'Output': clean_output})
        except:
            print('No output! Moving to next node...')
