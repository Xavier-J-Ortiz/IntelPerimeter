import pickle
import os
import re
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
#from watchdog.events import PatternMatchingEventHandler

from watchdog import watchmedo

perimeter = pickle.load(open('build-graph/perimeter.p', 'rb'))

file_path = '/home/xortiz/Documents/EVE/logs/Chatlogs/'
#file_path = '.'
chatlog_name = 'delve\.imperium'

#def find_files(file_path, chatlog_name):
date = datetime.datetime.utcnow()
year = date.strftime("%Y")
#raw_month = date.month
month = date.strftime("%m")
#raw_day = date.day
day = date.strftime("%d")
#files = os.listdir(file_path)
regex = '^' + file_path + chatlog_name + '_' + year + month + day + '.*'
#pattern = chatlog_name + '_' + year + month + day + '*'
#regex = re.compile('^' + chatlog_name + '_' + year + month + day + '.*')
#relevant = list(filter(regex.match, files))
#return relevant

if __name__ == "__main__":
    regexes = [regex, "^" + file_path + "Fleet.*"]
    ignore_regexes= []
    ignore_directories = False
    case_sensitive = True
    my_event_handler = RegexMatchingEventHandler(regexes,ignore_regexes,ignore_directories,case_sensitive)
    print (regexes)

    def on_modified(event):
        print(f"hey buddy, \'{event.src_path}\' has been modified")
        with open(event.src_path, 'r', encoding='utf-16') as changed_log:
            last_line = changed_log.readlines()[-1]
            print(last_line)

    
    my_event_handler.on_modified = on_modified

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, file_path, recursive=go_recursively)
    my_observer.schedule

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()