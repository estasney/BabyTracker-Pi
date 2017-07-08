import requests


def paramsbuilder(entryid, entrycontent):
    params = {}
    params[entryid] = entrycontent
    return params


def postgoogleform(form_url, params):
    r = requests.post(form_url, data=params, headers={"Content-type": "application/x-www-form-urlencoded"})
    return r.text








