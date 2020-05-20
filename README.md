# FYP_Agent

This repository contains the element of the Final Year Project which logs information about packages installed on Debian machines, along with their versions, and sends them to the [Central Administration Server (CAS)](https://github.com/TheFlyingPolak/FYP_CAS)

## Project Structre
- agent: contains the agent described above
- agent_console: contains a script used to send commands to the agent from its host device

## Agent structure
### ```run.py```
This is the entry point to the agent, run by the user to initialise the agent on a host device. This script will initialise contact with the CAS, schedule a cron job for package logging and start a HTTP handler to listen for commands.
Command line arguments:
- ```-u```: CAS IP and port as a single string in the format ```address:port``` (default - ```localhost:8080```)
- ```-t```: Package logging time interval in minutes (default: 60)
### ```runner.py```
This is the entry point for cron jobs. When ```run.py``` schedules the package logging cron job, it is scheduled to run ```runner.py```. This script also defines the Runner class. This creates a Logger object, which performs the logging operation, stores the log as ```log.json``` and sends it to the CAS. Contains a main method to allow crontab to run it. In normal operation it should not be run by a user directly.
Command line arguments:
- ```-u <address>```: CAS URL in the format ```http://address:port``` (default - ```http://localhost:8080```)
- ```-p <path>```: The path where the local copy of the log should be stored. By default stores in the same directory as this script
-```-i <id>```: The agent's ID. Does not run if unspecified.
### ```logger.py```
This script defines the Logger class, which performs the logging operation. It uses the dpkg package manager to get a table of installed packages and their versions, and returns them as a dictionary.

## Agent console
The agent console, located under "agent_console/agent_console.py" is used to send commands to the agent while it is running, from the same device as the agent is running on. The agent is listening for commands using a HTTP handler bound to port 8081. Commands are sent as a JSON string via a POST request.
Command line options:
- ```-n```: Prompt the agent to log package versions now
- ```-t <time>```: Prompt the agent to reschedule logging operation using specified time interval in minutes. Also causes the agent to log now

## Requirements
- Device running a Debian-based linux distribution (e.g. Debian, Ubuntu)
- Python 3
- python-crontab (install using ```pip install python-crontab```)
- Ports 8080 and 8081 open to the device running the agent

## How to use agent
- Copy the 'agent' directory anywhere on the device
- Ensure the CAS is running before starting the agent
- Start the agent using root priviledges (required for access to ports 8080 and 8081) using ```sudo python3 run.py -u <CAS IP:port> [-t <time in minutes>]```
