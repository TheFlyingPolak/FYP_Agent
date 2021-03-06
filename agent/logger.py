from collections import OrderedDict
import os
import re
import subprocess
from datetime import datetime


class Logger:
    regex = 'Name\s*Version\s*Architecture\s*Description'

    def __init__(self, path, agent_id):
        self._file_path = path
        self.id = agent_id

    def log(self):
        log_dict = OrderedDict()
        log_dict['agentId'] = self.id
        date = datetime.now()
        date_string = date.strftime('%Y-%m-%d %H:%M:%S')
        log_dict['timestamp'] = date_string
        # get machine hostname and write to dictionary
        process = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=15)
        log_dict['hostname'] = out.decode('utf-8').replace(' ', '').replace('\n', '')

        # get machine OS name and version and write to dictionary
        process = subprocess.Popen(['cat', '/etc/os-release'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=15)
        os_release = out.decode('utf-8').split('\n')
        name = os_release[0].split('=')
        version = os_release[1].split('=')
        log_dict['osName'] = name[1].replace('"', '')
        log_dict['osVersion'] = version[1].replace('"', '')

        # get data on all installed packages and write to dictionary
        packages_list = []
        with open(self._file_path + 'log.txt', 'w+') as f:
            cmd = ['dpkg', '-l']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate(timeout=15)
            f.write(out.decode('utf-8'))

            f.seek(0, 0)
            line = f.readline()
            while re.search(Logger.regex, line) is None:
                line = f.readline()

            f.readline()
            line = f.readline()
            while line is not '':
                list_raw = line.split()
                package = {'name': list_raw[1], 'version': list_raw[2], 'architecture': list_raw[3]}
                packages_list.append(package.copy())
                line = f.readline()

            log_dict['packages'] = packages_list

        if os.path.exists(self._file_path + 'log.txt'):
            os.remove(self._file_path + 'log.txt')

        return log_dict
