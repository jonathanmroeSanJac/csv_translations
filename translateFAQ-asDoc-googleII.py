import re
import translators as ts
import json
import os
import pandas
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# command arguments
input_csv = os.path.join('C:\workspaces\SJCC\SourceDocs','sjcc_extracted_dialog_responses_1.csv')
stop_words = os.path.join('C:\workspaces\SJCC\SourceDocs','universal-words-SpanishToEnglish.csv')
output_csv = os.path.join('C:\workspaces\SJCC\SourceDocs','sjcc_extracted_dialog_responses_1-spanishTHREE.csv')
final_csv = os.path.join('C:\workspaces\SJCC\SourceDocs','sjcc_extracted_dialog_responses_1-spanish-final.csv')
wym_text = 'Hola. Me llamo Jota Eme.'
translated_text = []
link_text = []
new_trans = ''
x = re.compile('<a.+?<\/a>')


print(ts.google(wym_text)) #This is just a test to see if the translation API is working.

df = pandas.read_csv(input_csv, skipinitialspace=True, usecols=["id","text"]) # Pull the two columns from the spreadsheet.
print(df)
index_list = df['text'].tolist() # Turn the first column into a list
id_list = df['id'].tolist() # Turn the second column into a list

df_stop = pandas.read_csv(stop_words, skipinitialspace=True, usecols=["spanish_text","english_text"]) # Pull the two columns from the stop_words spreadsheet
stop_sp = df_stop['spanish_text'].tolist() # Turn the first column into a list
stop_en = df_stop['english_text'].tolist() # turn the second column into a list
stop_dict = zip(stop_sp,stop_en) # Bring the two lists together
stop_dict = dict(stop_dict) # create a dictionary of the list
#print(stop_dict)


for line in index_list:
    new_trans = ts.google(line, from_language='en', to_language='es')
    anchors = x.findall(line)
    for anchor in anchors:
        line = line.replace(anchor,'***')
        new_trans = ts.google(line, from_language='en', to_language='es')
    for anchor in anchors:
        new_trans = new_trans.replace('***', anchor, 1)
    for key, value in stop_dict.items():
        new_trans = new_trans.replace(key,value)
    translated_text.append(new_trans)
    print(new_trans)
    print('+' * 30)
    
pairs = {'id': id_list, 'text':index_list, 'sp_text': translated_text}

df = pandas.DataFrame.from_dict(pairs)

df.to_csv(output_csv)

print('Created ' + output_csv)
