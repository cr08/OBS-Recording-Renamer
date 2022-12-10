import obspython as S
import glob, win32gui, win32process, re, psutil, os, os.path
from pathlib import Path
from ctypes import windll
import urllib.request

class Data:
    OutputDir = None
    Extension = None
    ExtensionMask = None
    Remove_MKV = None
    Delay = None
    Debug = False
    RenameMode = None
    WindowCount = None
    ChannelName = None
    
# Placeholder calls to pull game and stream title from Twitch. Will be added properly to the code later.
# We'll be utilizing DecAPI which allows us to pull this data without any keys or auth. A note will be added
# to the README in case this service ever fails in the future.

# twitch_streamtitle = urllib.request.urlopen("https://decapi.me/twitch/title/" + Data.ChannelName).read()
# twitch_game = urllib.request.urlopen("https://decapi.me/twitch/game/" + Data.ChannelName).read()

def on_event(event):

    if event == S.OBS_FRONTEND_EVENT_RECORDING_STOPPED:

        print("Triggered when the recording stopped")
        path = find_latest_file(Data.OutputDir, '\*')
        dir = os.path.dirname(path)
        rawfile = os.path.basename(path)
        title = get_window_title()
        newfile = rawfile[:-4]+' - ' + title + '.'+Data.Extension
        
        file = rawfile[:-3]+Data.Extension
        oldPath = dir +'\\'+ file

        f = open(oldPath[:-3]+"txt", "w")
        f.write(newfile)
        f.close()

        print(file)
        print(oldPath)
        print(newfile)

    if event == S.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        print("Triggered when the recording started. Window log cleaned and started.")
        with open(script_path()+'/WindowLog.txt') as winlist:
            if os.path.exists(winlist):
                os.remove(winlist)
                print("DEBUG: WindowLog.txt file found. Deleting and starting clean log.")
            else:
                print("DEBUG: No WindowLog.txt file found. Ignoring.")
    
    if event == S.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:

        print("Triggered when the replay buffer saved")
        path = find_latest_file(Data.OutputDir, '\*')
        dir = os.path.dirname(path)
        rawfile = os.path.basename(path)
        title = get_window_title()
        newfile = rawfile[:-4]+' - ' + title + '.'+Data.Extension
        
        file = rawfile[:-3]+Data.Extension
        oldPath = dir +'\\'+ file

        f = open(oldPath[:-3]+"txt", "w")
        f.write(newfile)
        f.close()

        print(file)
        print(oldPath)
        print(newfile)




def rename_files(directory):
    print("Processing files in " + directory)
    for txtfile in os.listdir(directory):
        if txtfile.endswith(".txt"):
            newfile = open(os.path.join(directory, txtfile), 'r').read()
            mkvfile = txtfile[:-3]+'mkv'
            mp4file = txtfile[:-3]+Data.Extension

            try:
                os.rename(os.path.join(directory, mp4file), os.path.join(directory, newfile))
                os.remove(os.path.join(directory, txtfile))
                if Data.Remove_MKV:
                    os.remove(os.path.join(directory, mkvfile))
            except WindowsError:
                print("Error, no file renamed")
        else:
            continue


def get_window_title():

    user32 = windll.user32

    swd, sht = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Add in fullscreen detection here! 
    w = win32gui
    win_title = w.GetWindowText(w.GetForegroundWindow())
    
    l, t, r, b = w.GetWindowRect(w.GetForegroundWindow())
    wd, ht = r - l, b - t

    tid, pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
    p = psutil.Process(pid)
    exe = p.name()

    desktopOveride = 0
    fullscreenOveride = 0

    with open(script_path()+'/DesktopOverride.cfg') as dofile:
     if exe in dofile.read():
            desktopOveride = 1
    
    with open(script_path()+'/FullscreenOverride.cfg') as fsfile:
        if exe in fsfile.read():
            fullscreenOveride = 1

    if win_title[:3] == 'OBS':
        title = "Manual Recording"
    elif desktopOveride == 1:
        title = win_title
    else:
        if  wd == swd and ht == sht and fullscreenOveride == 0:
            title = win_title
        else:
            title = "Desktop"

    title = re.sub(r'[^0-9A-Za-z .-]', '', title)
    title = title[:50]

    return title


def find_latest_file(folder_path, file_type):

        files = glob.glob(folder_path + file_type)
        max_file = max(files, key=os.path.getctime)
        return max_file


def script_load(settings):
    S.obs_frontend_add_event_callback(on_event)


def script_update(settings):
    Data.OutputDir = S.obs_data_get_string(settings,"outputdir")
    Data.OutputDir = Data.OutputDir.replace('/','\\')
    Data.Extension = S.obs_data_get_string(settings,"extension")
    Data.ExtensionMask = '\*' + Data.Extension
    Data.Remove_MKV = S.obs_data_get_bool(settings,"remove_mkv")
    Data.Delay = 1000*S.obs_data_get_int(settings,"period") or 15000
    Data.Debug = S.obs_data_get_bool(settings,"debug") or False
    Data.WindowCount = S.obs_data_get_int(settings,"windowcount") or 1
    

    print(Data.Delay)
    S.timer_remove(timer_process)
    S.timer_add(timer_process, Data.Delay)

def timer_process():
    print("timer activated")
    print(S.obs_service_get_username)
    rename_files(Data.OutputDir)


def script_description():
    "Triggers either when the recording is stopped, or the replay buffer is saved."


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_path(
        props, "outputdir", "Recordings folder", S.OBS_PATH_DIRECTORY,
        None, str(Path.home()))
    S.obs_properties_add_text(
        props,"extension","File extension",S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_int(
        props,"period","Time interval (s)", 15, 3600, 15)
    S.obs_properties_add_bool(
        props,"remove_mkv","Remove .mkv on rename?")
    print("lol")
    print(S.obs_properties_add_bool(props,"debug", "Enable debug logging for this script") + " lol " + S.obs_properties_add_bool(props,"debug2", "Test debug2"))
    S.obs_properties_add_int(
        props,"windowcount", "Specify how many windows during this session will be included in the filename, sorted by longest running.", 1, 99, 1)


    return props
