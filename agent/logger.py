from collections import OrderedDict
import os
import re
import subprocess


class Logger:
    regex = 'Name\s*Version\s*Architecture\s*Description'

    def __init__(self, path):
        self._file_path = path

    def log(self):
        log_dict = OrderedDict()
        # get machine hostname and write to dictionary
        process = subprocess.Popen(['hostname', '--fqdn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=15)
        log_dict['host_name'] = out.decode('ascii').replace('\n', '')

        # get machine OS name and version and write to dictionary
        process = subprocess.Popen(['cat', '/etc/os-release'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=15)
        os_release = out.decode('ascii').split('\n')
        name = os_release[0].split('=')
        version = os_release[1].split('=')
        log_dict['os_name'] = name[1].replace('"', '')
        log_dict['os_version'] = version[1].replace('"', '')

        # get data on all installed packages and write to dictionary
        packages_list = []
        with open(self._file_path + 'log.txt', 'w+') as f:
            cmd = ['dpkg', '-l']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate(timeout=15)
            f.write(out.decode('ascii'))

            f.seek(0, 0)
            line = f.readline()
            while re.search(Logger.regex, line) is None:
                line = f.readline()

            f.readline()
            line = f.readline()
            while line is not '':
                list_raw = line.split()
                separator = ' '
                package = {'name': list_raw[1], 'version': list_raw[2], 'architecture': list_raw[3],
                           'description': separator.join(list_raw[4:])}
                packages_list.append(package.copy())
                line = f.readline()

            log_dict['packages'] = packages_list

        #if os.path.exists(self._file_path + 'log.txt'):
        #    os.remove(self._file_path + 'log.txt')

        return log_dict
