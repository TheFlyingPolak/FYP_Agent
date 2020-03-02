import getopt, json, requests, sys


def main(argv):
    time = None
    try:
        opts, args = getopt.getopt(argv, 'nt:', ['now', 'time='])
    except getopt.GetoptError:
        print('Usage: agent_console.py --now --time <logging time interval>')
        print('                           -n     -t')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-n', '--now'):
            pass
        elif opt in ('-t', '--time'):
            time = int(arg)

    command = {}
    if time is None:
        command['command'] = 'log_now'
    else:
        command['command'] = 'change_log_time_interval'
        command['time'] = time

    url = 'http://localhost:8081/command'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(command), headers=headers)

    if r.status_code == 200:
        print('Success')
    else:
        print('Something went wrong')


if __name__ == '__main__':
    main(sys.argv[1:])
