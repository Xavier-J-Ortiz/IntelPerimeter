import vlc, time, datetime, json,os
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
from termcolor import colored
from build_graph.create_perimeter import create_perimeter
from build_graph.node_graph_builder import build_graph

config = json.load(open('./config.json',))
node_graph = build_graph()
perimeter = create_perimeter(config['central_system'], node_graph, config['jumps'])
file_path = os.path.expanduser(config['chatlog_path'])
channel_names = config['channel_names']

date = datetime.datetime.utcnow()
year = date.strftime("%Y")
month = date.strftime("%m")
day = date.strftime("%d")

if __name__ == "__main__":
    regexes = []
    for channel in channel_names:
        regex = '^' + file_path + channel + '_' + year + month + day + '.*'
        regexes.append(regex)
    ignore_regexes= []
    ignore_directories = False
    case_sensitive = True
    my_event_handler = RegexMatchingEventHandler(regexes,ignore_regexes,ignore_directories,case_sensitive)

    def on_modified(event):
        with open(event.src_path, 'r', encoding='utf-16') as changed_log:
            last_line = changed_log.readlines()[-1]
            analyze = last_line.replace('\n',' ').split(" ")
            analyze_lowercase = [entry.lower() for entry in analyze]
            zero_system = ''
            for system in perimeter:
                if perimeter[system] == 0:
                    zero_system = system
            print(last_line)
            for system in perimeter:
                if system.lower() in analyze_lowercase:
                    print(colored(f'\n-----\nDANGER: {system} : {perimeter[system]} jumps out from {zero_system}\n-----\n', 'red')) 
                    alarm = vlc.MediaPlayer('alarms/alarm2.mp3')
                    alarm.play()

    
    my_event_handler.on_modified = on_modified

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, file_path, recursive=go_recursively)
    my_observer.schedule

    my_observer.start()
    print("watcher.py is running")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()