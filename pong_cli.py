#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import requests

def start_game(pong_time_ms):
    requests.post("http://localhost:8000/start", json={"pong_time": pong_time_ms})
    requests.post("http://localhost:8001/start", json={"pong_time": pong_time_ms})
    requests.get("http://localhost:8000/ping?target=localhost:8001")

def pause_game():
    requests.post("http://localhost:8000/pause")
    requests.post("http://localhost:8001/pause")

def resume_game():
    requests.post("http://localhost:8000/resume")
    requests.post("http://localhost:8001/resume")

def stop_game():
    requests.post("http://localhost:8000/stop")
    requests.post("http://localhost:8001/stop")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pong_cli.py <command> [<param>]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) < 3:
            print("Usage: python pong_cli.py start <pong_time_ms>")
            sys.exit(1)
        pong_time_ms = int(sys.argv[2])
        start_game(pong_time_ms)
    elif command == "pause":
        pause_game()
    elif command == "resume":
        resume_game()
    elif command == "stop":
        stop_game()
    else:
        print(f"Unknown command: {command}")

