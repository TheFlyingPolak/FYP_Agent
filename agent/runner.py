from logger import Logger
import json
import requests


class Runner:
    def __init__(self, url, time, path):
        self._server_url = url
        self.log_time = time
        self._log_file_path = path + '/log.json'
        self._logger = Logger(path)
        log_json = self._log()

        url = self._server_url + '/agents'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        r = requests.post(url, data=open('./log.json', 'rb'), headers=headers)

        if r.status_code == 200:
            self._id_number_string = r.text
            self.run()

    def run(self):
        log_json = self._log()
        url = self._server_url + '/agents/' + self._id_number_string
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        r = requests.put(url, data=open('./log.json', 'rb'), headers=headers)

    def _log(self):
        log_dict = self._logger.log()
        log_json = json.dumps(log_dict)
        with open('./log.json', 'w') as f:
            json.dump(log_dict, f)

        return log_json
