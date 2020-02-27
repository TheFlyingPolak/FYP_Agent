from runner import Runner
import getopt
import sys


def main(argv):
    url = 'localhost:8080'
    time = '60'
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
            time = arg

    url = 'http://' + url
    runner = Runner(url, time, '')


if __name__ == '__main__':
    main(sys.argv[1:])
