#!usr/bin/python3

from logger import Logger
import getopt
import json
import requests
import sys
from datetime import datetime


class Runner:
    def __init__(self, url, path, agent_id):
        self._server_url = url
        self._log_file_path = path + '/log.json'
        if agent_id is None:
            self._id_number_string = '-1'
        else:
            self._id_number_string = agent_id
        self._logger = Logger(path, self._id_number_string)

    def initialise(self):
        log_json = self._log()
        url = self._server_url + '/agents'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        payload = {'json_payload': log_json}
        r = requests.post(url, data=log_json, headers=headers)
        if r.status_code == 200:
            self._id_number_string = r.text
            self._logger.id = self._id_number_string
            self.run()
        return self._id_number_string

    def run(self):
        log_json = self._log()
        url = self._server_url + '/agents/' + self._id_number_string
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        payload = {'json_payload': log_json}
        r = requests.put(url, data=log_json, headers=headers)

    def _log(self):
        log_dict = self._logger.log()
        log_json = json.dumps(log_dict)
        with open('./log.json', 'w') as f:
            json.dump(log_dict, f)

        return log_json


def main(argv):
    url = 'http://localhost:8080'
    path = ''
    agent_id = ''

    try:
        opts, args = getopt.getopt(argv, 'u:p:i:', ['url=', 'path=', 'id='])
    except getopt.GetoptError:
        print('Usage: runner.py --url <server url> --path <file path> --id <agent id>')
        print('                    -u <server url>     -p <file path>   -i <agent id>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-u', '--url'):
            url = 'http://' + arg
        elif opt in ('-p', '--path'):
            path = arg
        elif opt in ('-i', '--id'):
            agent_id = arg

    runner = Runner(url, path, agent_id)
    print('URL: ' + url)
    if agent_id == '':
        print('Agent id not given. Agent will not log.')
    else:
        print('Running logger at ' + datetime.now().strftime('%H:%M:%S'))
        runner.run()


if __name__ == '__main__':
    main(sys.argv[1:])
