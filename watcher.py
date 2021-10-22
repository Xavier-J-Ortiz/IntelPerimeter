from build_graph.system_puller import get_systems
import pickle, vlc, time, datetime
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
from termcolor import colored
from build_graph.system_puller import get_systems
from build_graph.stargate_builder import get_system_stargates
from build_graph.neighbor_builder import get_systems_neighbors
from build_graph.node_builder import get_node_names
from build_graph.create_perimeter import create_perimeter

all_systems = get_systems()
error_write_neighbor = open("output_neighbor.txt","w+")
error_write_stargate = open("output_stargate.txt","w+")
systemsAndGates = {}
systemsAndGates = get_system_stargates(all_systems, systemsAndGates, error_write_stargate)
systemsAndNeighbors = get_systems_neighbors(all_systems, systemsAndGates, error_write_neighbor)
nodes = get_node_names(all_systems, systemsAndNeighbors)
node_graph = pickle.load(open('./data/nodes.p', 'rb'))
perimeter_dict = create_perimeter('K-6K16', node_graph, 3)
print(perimeter_dict)

# should be input by user
file_path = '/home/xortiz/Games/eve-online/drive_c/users/xortiz/Documents/EVE/logs/Chatlogs/'
# should be input by user
channel_names = ['delve\.imperium', 'Fleet', 'querious\.imperium']
#should be built by user
perimeter = pickle.load(open('data/perimeter.p', 'rb'))

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
            #print(zero_system)
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
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

