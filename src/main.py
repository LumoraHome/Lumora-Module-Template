from enum import Enum
import os
import sys
import json

class job_status(Enum):
    ERROR = -1
    RUNNING = 0
    SUCCESS = 1

class commands(Enum):
    UPDATE_STATUS="update_status"
    DEBUG="debug"
    JOB_UPDATE="job_update"

def send(command, args):
    payload = json.dumps({
        "command": command,
        "args": args,
    }) + "\n"

    sys.stdout.write(payload)
    sys.stdout.flush()

def handle_command(cmd):
    if not "command" in cmd or not "args" in cmd:
        return None
    match cmd["command"]:
        case "start":
            send(command=commands.UPDATE_STATUS.value, args=["running", cmd["args"][0]])
            send(command=commands.DEBUG.value, args=["started"])
        case "stop":
            send(command=commands.UPDATE_STATUS.value, args=["stopped", cmd["args"][0]])
            send(command=commands.DEBUG.value, args=["stopped"])
        case _:
            send(command=commands.JOB_UPDATE.value, args=[job_status.SUCCESS.value, cmd["args"][-1]])
            send(command=commands.DEBUG.value, args=[cmd["command"], cmd["args"][-1]])

send(command="update_status", args=["initialized"])

while True:
    line = sys.stdin.readline()
    if not line: break
    try:
        command = json.loads(line)
        handle_command(command)
    except json.JSONDecodeError as e:
        pass
