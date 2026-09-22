import os
import sys
import json

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
            send(command="update_status", args=["running", cmd["args"][0]])
            send(command="debug", args=["started"])
        case "stop":
            send(command="update_status", args=["stopped", cmd["args"][0]])
            send(command="debug", args=["stopped"])
        case _:
            send(command="debug", args=[cmd["command"], cmd["args"][-1]])

send(command="update_status", args=["initialized"])

while True:
    line = sys.stdin.readline()
    if not line: break
    try:
        command = json.loads(line)
        handle_command(command)
    except json.JSONDecodeError as e:
        pass
