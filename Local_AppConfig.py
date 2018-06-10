import pickle


def read_key(path):
    with open(path, 'rb') as pfile:
        key = pickle.load(pfile)
        return key

class AppConfig(object):
    form_url = ""
    entryid_action = ''
    entryid_local_time = ''
    backup_csv = ''
    sqlite_db = 'tracker.db'
    log_to_google = False
    log_to_csv = False
    log_to_pkl = False
    log_to_gui = False
    log_to_tally = False
    log_to_sql = True


class ApiConfig(object):

    api_key_path = 'weather_key.pkl'
    api_key = read_key(api_key_path)
    city_id = 4467657

