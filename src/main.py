import sys
import json

def handle_command(cmd):
    if not "command" in cmd or not "id" in cmd:
        return None
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

sys.stdout.write('{"command":"update_status", "args":["initialized"]}\n')
sys.stdout.flush()

for line in sys.stdin:
    try:
        command = json.loads(line)
        response = handle_command(command)
        print(json.dumps(response), flush=True)
    except json.JSONDecodeError as e:
        pass
