from runner import Runner
import getopt
import json
import sched
import sys
import threading
import time
import socketserver
from http.server import BaseHTTPRequestHandler


def main(argv):
    url = 'localhost:8080'      # the address of the server to communicate with
    log_time = '60'     # log time is in minutes
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

    url = 'http://' + url
    runner = Runner(url, log_time, '')

    s = sched.scheduler(time.time, time.sleep)

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == '/command':
                if self.headers['Content-Type'] == 'application/json':
                    content_length = int(self.headers['Content-Length'])
                    command_data = self.rfile.read(content_length)
                    command_json = json.loads(command_data.decode('utf-8'))
                    if command_json['command'] == 'log_now':
                        print('log now')
                        #s.run()   doesn't work
                    elif command_json['command'] == 'change_log_time_interval':
                        print('change log time interval')
                    #    s.enter(int(command_json['time']) * 60, 1, timer, (s,))
                    #    s.run()    doesn't work
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    # command listening thread
    def command():
        httpd = socketserver.TCPServer(('', 8081), Handler)
        httpd.serve_forever()

    command_thread = threading.Thread(target=command, daemon=True)
    command_thread.start()

    # logging event
    def timer(sc):
        runner.run()
        s.enter(int(log_time) * 60, 1, timer, (sc,))

    s.enter(int(log_time) * 60, 1, timer, (s,))
    s.run()


if __name__ == '__main__':
    main(sys.argv[1:])
