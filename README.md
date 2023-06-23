# OBS-Rec-Rename

This script automatically renames the recording once stopped to include extra useful info such as the game window/title or Twitch stream name. As of version 1.0, only the Twitch channel, game name, and stream title are used to produce the following filenames:

`<original filename format as configured in OBS> - VOD/REP - Channel - Game Name - Stream Title.ext`

## Installation

* Please install a version of Python 3.6 or newer. This has been tested and is functional with 3.10 on my personal machine.
* Launch OBS and open the Scripts menu by going to `Tools > Scripts` and select the `Python Settings` tab
* Browse toward your Python install path where `python.exe` is located. This will vary depending on your install method. Once properly configured, the dialog should display `Loaded Python Version: 3.xx` below
* Once Python is configured, return to the `Scripts` tab and add `RecordingRenamer.py` and configure the script accordingly (additional documentation for the available options in the Usage section below)
  * NOTE: This script can be placed anywhere on your system. It does not need to be stored with the recordings and is advised against.

## Usage

Once the `RecordingRenamer.py` script is added to OBS, you will be provided with a set of options:

- Recordings Folder: The folder OBS outputs the recordings to. This should match what is in `Settings > Output > Recording > Recording Path`
- Rename Mode: This selects the source of the filename details. At this time, only `Twitch Game/Stream title` is available.
- Twitch Channel: Your Twitch channel name. This is required to pull your game/stream title info
- Rename Replays?: Allows you to toggle if you want the script to rename your saved replays or default to the stock OBS functionality
- Enable debug: As it says on the tin. I've included a ton of debugging lines that go to the script log in case things break.

The script will then run whenever a recording is finished, or an instant replay buffer is saved.

## Changelog

##### 1.1

* Fixed filename formatting. Code was previously written by accident to include the game name twice and not include the stream title. This is corrected and should follow the example shown at the top of this README.

##### 1.0

* Basic functionality complete with the Twitch game name/stream title source to start with
  * Twitch info polling is provided through DecAPI.me - No keys or or special credentials required, just your channel name
* Old window title code commented out for now. This needs a more significant overhaul for the functionality I want to implement
* Timer code commented out - With only the Twitch mode active, we'll trigger the rename process at the time of the stopped recording instead of waiting for the timer loop to cycle. Saves on extra log spam and a negligible amount of extra processing
* File extension code streamlined. We now poll the extension of the recordings automatically and maintain it after renaming.
