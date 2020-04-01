from runner import Runner
import getopt
import json
import os
import signal
import sys
import socketserver
import subprocess
from crontab import CronTab
from http.server import BaseHTTPRequestHandler

job_comment = 'agent'
cron = CronTab(user=True)


def main(argv):
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    url = 'localhost:8080'      # the address of the server to communicate with
    log_time = '60'     # log time is in minutes
    agent_id = ''
    try:
        opts, args = getopt.getopt(argv, 'u:t:', ['url=', 'time='])
    except getopt.GetoptError:
        print('Usage: run.py -u <server url> -t <logging time interval>')
        print('              --url <server url> --time <logging time interval>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-u', '--url'):
            url = arg
        elif opt in ('-t', '--time'):
            log_time = arg

    runner = Runner('http://' + url, '', None)
    agent_id = runner.initialise()
    command = '/usr/bin/python3 ' + os.getcwd() + '/runner.py -u ' + url + ' -i ' + agent_id
    remove_job_if_exists()
    job = cron.new(command=command, comment=job_comment)
    print('cron will run every', log_time, 'minutes')
    log_time_int = int(log_time)
    job.minute.every(log_time_int)
    cron.write()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == '/command':
                if self.headers['Content-Type'] == 'application/json':
                    content_length = int(self.headers['Content-Length'])
                    command_data = self.rfile.read(content_length)
                    command_json = json.loads(command_data.decode('utf-8'))
                    if command_json['command'] == 'log_now' or command_json['command'] == 'change_log_time_interval':
                        nonlocal log_time
                        if command_json['command'] == 'change_log_time_interval':
                            log_time = command_json['time']
                        reschedule_job(command, log_time)
                        subprocess.run(command.split(" "))

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

    # command listening thread
    httpd = socketserver.TCPServer(('', 8081), Handler)
    httpd.serve_forever()


def remove_job_if_exists():
    for job in cron:
        if job.comment == job_comment:
            cron.remove(job)
            cron.write()


def reschedule_job(command, time):
    remove_job_if_exists()
    job = cron.new(command=command, comment=job_comment)
    job.minute.every(int(time))
    cron.write()


def signal_handler(sig, frame):
    print('Agent is terminating...')
    remove_job_if_exists()
    exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
