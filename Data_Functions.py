import requests
import csv

def params_builder(entry_ids, entry_contents):
    param_dict = {}
    for id_num, content in zip(entry_ids, entry_contents):
        param_dict[id_num] = content
    return param_dict


def post_google_form(form_url, params, backup_csv):
    with open(backup_csv, "a+", encoding='utf-8', newline='') as csv_file:
        outputwriter = csv.writer(csv_file, dialect='excel')
        values_to_write = []
        for key, value in params.items():
            values_to_write.append(value)
        outputwriter.writerow(values_to_write)

        try:
            r = requests.post(form_url, data=params, headers={"Content-type": "application/x-www-form-urlencoded"})
            return r.text
        except:
            return "Error Posting To Google"

