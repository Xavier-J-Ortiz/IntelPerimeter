#!/usr/bin/env python3
import datetime
import json
import os
import time
import mpv

from termcolor import colored
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer

from build_graph.create_perimeter import create_perimeter
from build_graph.node_graph_builder import build_graph

node_graph = build_graph()
with open("./config.json", 'r', encoding="utf-8") as config_file:
    config = json.load(config_file)
perimeter = create_perimeter(config["central_system"], node_graph, config["jumps"])
file_path = os.path.expanduser(config["chatlog_path"])
channel_names = config["channel_names"]
alarm = mpv.MPV()

date = datetime.datetime.now(datetime.UTC)
year = date.strftime("%Y")
month = date.strftime("%m")
day = date.strftime("%d")

if __name__ == "__main__":
    regexes = []
    for channel in channel_names:
        regex = "^" + file_path + channel + "_" + year + month + day + ".*"
        regexes.append(regex)
    ZERO_SYSTEM = ""
    for system, jumps in perimeter.items():
        if jumps == 0:
            ZERO_SYSTEM = system
    ignore_regexes: list[str] = []
    IGNORE_DIRECTORIES = False
    CASE_SENSITIVE = True
    my_event_handler = RegexMatchingEventHandler(
        regexes=regexes, ignore_regexes=ignore_regexes, ignore_directories=IGNORE_DIRECTORIES, case_sensitive=CASE_SENSITIVE
    )
    last_line_set = set()

    def on_modified(event):
        with open(event.src_path, "r", encoding="utf-16") as changed_log:
            log_line = changed_log.readlines()[-1]
            last_line_set.add(log_line)

    my_event_handler.on_modified = on_modified
    GO_RECURSIVELY = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, file_path, recursive=GO_RECURSIVELY)
    my_observer.start()
    print("watcher.py is running")
    try:
        while True:
            time.sleep(1)
            if len(last_line_set) > 0:
                for line in last_line_set:
                    last_line = line
                    analyze = last_line.replace("\n", " ").split(" ")
                    analyze_lowercase = [entry.lower() for entry in analyze]
                    print(last_line)
                    for system, jumps in perimeter.items():
                        if system.lower() in analyze_lowercase:
                            print(
                                colored(
                                    f"\n-----\nDANGER: {system} : {jumps} jumps out from {ZERO_SYSTEM}\n-----\n",
                                    "red",
                                )
                            )
                            alarm.play("alarms/alarm2.mp3")
                last_line_set = set()
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
