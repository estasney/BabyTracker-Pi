import requests


def params_builder(entry_id, entry_content):
    params = {entry_id: entry_content}
    return params


def post_google_form(form_url, params):
    r = requests.post(form_url, data=params, headers={"Content-type": "application/x-www-form-urlencoded"})
    return r.text








