import obspython as S
import glob, os, os.path
from pathlib import Path
import urllib.request
# from datetime import datetime
import pywinctl as pwc


description = "<center><h2>OBS-Rec-Rename</h2></center><center><h3>Script to automatically rename recordings based on content.</h3></center><center><h4>Click <a href=\"https://github.com/cr08/obs-rec-rename#readme\">here</a> for documentation.<hr>"

class Data:
    OutputDir = None
    Delay = None
    Debug = False
    Replay_True = False
    RenameMode = None
    # WindowCount = None
    ChannelName = None
    
# Date code not needed for now since we keep the timestamp from the stock recording functionality
#
# now = datetime.now()
# timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')

def cleanFilename(sourcestring,  removestring ="\`/<>\:\"\\|?*"):
    return ''.join([c for c in sourcestring if c not in removestring])

def on_event(event):

    if event == S.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        if Data.Debug == True:
            print("DEBUG: Recording session STOPPED...") 
        path = find_latest_file(Data.OutputDir, '\*')
        dir = os.path.dirname(path)
        rawfile = os.path.basename(path)
        root_ext = os.path.splitext(rawfile)
        
        if Data.Debug == True:
            print("DEBUG: Original Filename: \"" + rawfile + "\"")
        
        if Data.RenameMode == 1:
            twitch_streamtitle = urllib.request.urlopen("https://decapi.me/twitch/title/" + str(Data.ChannelName)).read()
            twitch_game = urllib.request.urlopen("https://decapi.me/twitch/game/" + str(Data.ChannelName)).read()
            title = "VOD - " + Data.ChannelName + " - " + str(twitch_game.decode("utf-8")) + " - " + str(twitch_streamtitle.decode("utf-8"))
            title = cleanFilename(title)
            if Data.Debug == True:
                print("DEBUG: Twitch Mode: Channel - " + Data.ChannelName)
                print("DEBUG: Twitch Mode: Game - " + str(twitch_game.decode("utf-8")))
                print("DEBUG: Twitch Mode: Stream Title - " + str(twitch_streamtitle.decode("utf-8")))

        else:
            # title = get_window_title()
                if Data.Debug == True:
                    print("DEBUG: A rename mode other than 'Twitch Game/Stream title' was chosen. Only the Twitch mode is available at this time.")
                    
        newfile = root_ext[0] + " - " + title + root_ext[1]
        
        file = root_ext[0] + root_ext[1]
        oldPath = dir +'\\'+ file

        f = open(oldPath + ".txt", "w")
        f.write(newfile)
        f.close()
        
        rename_files(Data.OutputDir)

        if Data.Debug == True:
            print("DEBUG: Old file path - " + oldPath)
            print("DEBUG: New file path - " + dir + "\\" + newfile)            


    if event == S.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        if Data.Debug == True:
            print("DEBUG: Recording session started...")        
        # Commenting out the window title code for now. Initially we'll focus on just the Twitch stream info as the primary naming source
        #
        # print("Triggered when the recording started. Window log cleaned and started.")
        # with open(script_path()+'/WindowLog.txt') as winlist:
        #     if os.path.exists(winlist):
        #         os.remove(winlist)
        #         print("DEBUG: WindowLog.txt file found. Deleting and starting clean log.")
        #     else:
        #         print("DEBUG: No WindowLog.txt file found. Ignoring.")

    if event == S.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:
        if Data.Replay_True == True:
            if Data.Debug == True:
                print("DEBUG: Replay Buffer SAVED")
            path = find_latest_file(Data.OutputDir, '\*')
            dir = os.path.dirname(path)
            rawfile = os.path.basename(path)
            root_ext = os.path.splitext(rawfile)
            
            if Data.Debug == True:
                print("DEBUG: Original Filename: \"" + rawfile + "\"")
                
            if Data.RenameMode == 1:
                twitch_streamtitle = urllib.request.urlopen("https://decapi.me/twitch/title/" + str(Data.ChannelName)).read()
                twitch_game = urllib.request.urlopen("https://decapi.me/twitch/game/" + str(Data.ChannelName)).read()
                title = "REP - " + Data.ChannelName + " - " + str(twitch_game.decode("utf-8")) + " - " + str(twitch_streamtitle.decode("utf-8"))
                title = cleanFilename(title)
                if Data.Debug == True:
                    print("DEBUG: Twitch Mode: Channel - " + Data.ChannelName)
                    print("DEBUG: Twitch Mode: Game - " + str(twitch_game.decode("utf-8")))
                    print("DEBUG: Twitch Mode: Stream Title - " + str(twitch_streamtitle.decode("utf-8")))

            else:
                # title = get_window_title()
                if Data.Debug == True:
                    print("DEBUG: A rename mode other than 'Twitch Game/Stream title' was chosen. Only the Twitch mode is available at this time.")
                
            newfile = root_ext[0] + " - " + title + root_ext[1]
            
            file = root_ext[0] + root_ext[1]
            oldPath = dir +'\\'+ file

            f = open(oldPath + ".txt", "w")
            f.write(newfile)
            f.close()

            rename_files(Data.OutputDir)

            if Data.Debug == True:
                print("DEBUG: Old file path - " + oldPath)
                print("DEBUG: New file path - " + dir + "\\" + newfile)
        
        else:
            if Data.Debug == True:
                print("DEBUG: Replay buffer SAVED but we are not renaming replays. Skipping...")
            
    if event == S.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTED:
        
        if Data.Debug == True:
            print("DEBUG: Replay Buffer Started")
 
    if event == S.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPED:
        
        if Data.Debug == True:
            print("DEBUG: Replay Buffer Stopped")

def rename_files(directory):
    if Data.Debug == True:
        print("DEBUG: Processing files in " + directory)
    for txtfile in os.listdir(directory):
        if txtfile.endswith(".txt"):
            root_ext = os.path.splitext(txtfile)
            newfile = open(os.path.join(directory, txtfile), 'r').read()

            try:
                os.rename(os.path.join(directory, root_ext[0]), os.path.join(directory, newfile))
                os.remove(os.path.join(directory, txtfile))
            except WindowsError:
                print("ERROR: No file renamed")
        else:
            continue

def get_foreground_window():
    if Data.Debug == True:
        print("DEBUG: Current window: \"" + pwc.getActiveWindowTitle() + "\"")

def find_latest_file(folder_path, file_type):

        files = glob.glob(folder_path + file_type)
        max_file = max(files, key=os.path.getctime)
        return max_file

def script_load(settings):
    S.obs_frontend_add_event_callback(on_event)

def script_update(settings):
    Data.OutputDir = S.obs_data_get_string(settings,"outputdir")
    Data.OutputDir = Data.OutputDir.replace('/','\\')
    Data.DelayOld = Data.Delay
    Data.Delay = 1000*S.obs_data_get_int(settings,"period") or 5000
    Data.Debug = S.obs_data_get_bool(settings,"debug") or False
    Data.Replay_True = S.obs_data_get_bool(settings,"replay_true") or False
    # Data.WindowCount = S.obs_data_get_int(settings,"windowcount") or 1
    Data.RenameMode = S.obs_data_get_int(settings,"mode")
    Data.ChannelName = S.obs_data_get_string(settings, "twitch_channel")

    if Data.Debug == True:
        print("DEBUG: Script updating...")
        print("DEBUG: Interval - " + str(Data.Delay))
        print("DEBUG: Debug - " + str(Data.Debug))
    
        if Data.RenameMode == 0:
            print("DEBUG: RenameMode - Active Window(s) title - " + str(Data.RenameMode))  
        elif Data.RenameMode == 1:
            print("DEBUG: RenameMode - Twitch Game/Stream title - " + str(Data.RenameMode))
            print("DEBUG: Twitch Channel - " + str(Data.ChannelName))
        elif Data.RenameMode == 2:
            print("DEBUG: RenameMode - Active Scene(s) - " + str(Data.RenameMode))
        elif Data.RenameMode == 3:
            print("DEBUG: RenameMode - Active Game/Window Capture Source(s) - " + str(Data.RenameMode))
        elif Data.RenameMode == 4:
            print("DEBUG: RenameMode - OBS Profile Name - " + str(Data.RenameMode))   
        elif Data.RenameMode == 5:
            print("DEBUG: RenameMode - OBS Scene Collection Name - " + str(Data.RenameMode))
        print("DEBUG: Rename Replays - " + str(Data.Replay_True))
    
    if Data.Delay != Data.DelayOld:
        if Data.Debug == True:
            print("DEBUG: Time interval changed. Restarting timer_process.")

        S.timer_remove(timer_process)
        S.timer_add(timer_process, Data.Delay)

def timer_process():
    print("timer activated")
    # rename_files(Data.OutputDir)
    get_foreground_window()


def script_description():
    return description


def script_properties():
    props = S.obs_properties_create()
    outputdir_p = S.obs_properties_add_path(
        props, "outputdir", "Recordings Folder", S.OBS_PATH_DIRECTORY,
        None, str(Path.home()))
    period_p = S.obs_properties_add_int(
        props,"period","Time interval (s)", 5, 3600, 5)
    
    mode_p = S.obs_properties_add_list(
        props,"mode","Rename Mode",S.OBS_COMBO_TYPE_LIST,S.OBS_COMBO_FORMAT_INT)
    # S.obs_property_list_add_int(
    #     mode_p,"Most active foreground window(s) during recording session.", 0)
    S.obs_property_list_add_int(
        mode_p,"Twitch Game/Stream title", 1)
    # S.obs_property_list_add_int(
    #     mode_p, "Most active scene name", 2)
    # S.obs_property_list_add_int(
    #     mode_p, "Most active game or window capture source", 3)
    # S.obs_property_list_add_int(
    #     mode_p, "OBS Profile name", 4)
    # S.obs_property_list_add_int(
    #     mode_p, "OBS Scene Collection name", 5)

    
    # S.obs_properties_add_int(
    #     props,"windowcount", "Window count", 1, 99, 1)
    twitch_channel_p = S.obs_properties_add_text(
        props,"twitch_channel","Twitch Channel",S.OBS_TEXT_DEFAULT)
    replay_true_p = S.obs_properties_add_bool(
        props,"replay_true", "Rename Replays?")
    debug_p = S.obs_properties_add_bool(
        props,"debug", "Enable Debug")
    

    return props
