import sys
import json

def handle_command(cmd):
    if cmd["command"] == "start":
        return {
            "id": cmd["id"],
            "success": True,
            "status": "started"
        }

    if cmd["command"] == "stop":
        return {
            "id": cmd["id"],
            "success": True,
            "status": "stopped"
        }

    if cmd["command"] == "command":
        return {
            "id": cmd["id"],
            "success": True,
            "status": "ran"
        }

for line in sys.stdin:
    command = json.loads(line)

    response = handle_command(command)

    print(json.dumps(response), flush=True)