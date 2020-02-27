from runner import Runner
import getopt
import sched
import sys
import threading
import time


def main(argv):
    running = True
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

    while running:
        time.sleep(float(log_time) * 60)
        runner.run()


if __name__ == '__main__':
    main(sys.argv[1:])
