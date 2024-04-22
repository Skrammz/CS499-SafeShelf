import os
import pandas as pd
import sys

sys.path.insert(0, r"c:\users\user\appdata\local\programs\python\python39\lib\site-packages")

f = open("txt.txt", "r")
temp = f.readline()
os.system(temp)
def column_switch(df, column1, column2):
    i = list(df.columns)
    a, b = i.index(column1), i.index(column2)
    i[b], i[a] = i[a], i[b]
    df.columns = i
    return df
def mainFunc():
	with open("./modified.json") as f:
		temp = pd.read_json(f)
		temp.to_csv("data_file.csv", index=False)
def nameChange():
        with open("./hi.json") as f:
                data = pd.read_json(f)
                header_mapping = {'field_title': 'Title',
                                  'field_last_modified_date' : 'Date Issued',
                                  'field_recall_type': 'Recall Status',
                                  'field_states': 'States',
                                  'field_establishment': 'Company',
                                  'field_recall_classification': 'Recall Classification',
                                  'field_recall_reason': 'Recall Reason'}
                data = data.drop(["field_archive_recall", "field_closed_date",
                                  "field_closed_year", "field_company_media_contact",
                                  "field_closed_date", "field_distro_list",
                                  "field_en_press_release", "field_labels",
                                  "field_media_contact", "field_recall_date",
                                  "field_press_release", "field_processing",
                                  "field_product_items", "field_qty_recovered",
                                  "field_closed_date", "field_recall_number",
                                  "field_active_notice", "field_related_to_outbreak",
                                  "field_summary", "field_year", "langcode",
                                  "field_has_spanish", "field_risk_level"], axis = 1)
                data = data.rename(columns = header_mapping)
                columns_titles = ["Company", "Title", "States", "Date Issued", "Recall Reason",
                                  "Recall Status", "Recall Classification"]
                data = data.reindex(columns = columns_titles)
                data.to_json('modified.json', orient = 'records', indent = 4)
nameChange()
mainFunc()