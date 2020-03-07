from runner import Runner
import getopt
import json
import sys
import socketserver
from crontab import CronTab
from http.server import BaseHTTPRequestHandler


def main(argv):
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

    runner = Runner('http://' + url, '', '')
    agent_id = runner.initialise()
    open('tabfile.tab', 'w')
    cron = CronTab(user=True)
    command = '/usr/bin/python3 /home/student/agent/runner.py -u ' + url + ' -i ' + agent_id
    job = cron.new(command=command)
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
                    if command_json['command'] == 'log_now':
                        print('log now')
                    elif command_json['command'] == 'change_log_time_interval':
                        print('change log time interval')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    # command listening thread
    httpd = socketserver.TCPServer(('', 8081), Handler)
    httpd.serve_forever()


if __name__ == '__main__':
    main(sys.argv[1:])
