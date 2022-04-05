#---------------------------
# Import Libraries
#---------------------------
import os
import sys
import json
import time
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# Import your Settings class
from Settings_Module import MySettings

# Import VK class
from Keyboard_Module import VK, StrikeKey

#---------------------------
# Script Information
#---------------------------
ScriptName = "Auto Instant Replay"
Website = "https://www.twitch.tv/iBroadband"
Description = "Chatters use !replay to request an instant replay"
Creator = "iBroadband"
Version = "1.0.8"

#---------------------------
# Define Global Variables
#---------------------------
global SettingsFile
global ScriptSettings
global InstantReplayRequestCount
global BridgeApp
global MostRecentRequest
global VK
global UserHotkey

SettingsFile = ""
ScriptSettings = MySettings()
InstantReplayRequestCount = 0
BridgeApp = os.path.join(os.path.dirname(__file__), "bridge\\SLOBSRC.exe")
MostRecentRequest = datetime.now()
VK = VK()
UserHotkey = VK.f12

#---------------------------
# Initialize Data (Only called on load)
#---------------------------
def Init():
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)

    # Initialize Instant Replay params
    InstantReplayRequestCount = 0
    MostRecentRequest = datetime.now()
    UserHotkey = ParseUserHotkey(ScriptSettings.Hotkey)

    return

#---------------------------
# Execute Data / Process messages
#---------------------------
def Execute(data):

    #   Check if the incoming message is a command
    if (data.IsChatMessage() and
        data.GetParam(0).lower() == ScriptSettings.Command):

        # User is on cooldown
        if (Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User)):
            Parent.SendStreamWhisper(data.User, "!replay Cooldown: " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))

        # Command is on cooldown
        if (Parent.IsOnCooldown(ScriptName, ScriptSettings.Command)):
            #if (ScriptSettings.AlertChat):
                #Parent.SendStreamMessage(ScriptSettings.Command + " is on cooldown.")
            pass

        # Command is ready to go
        if (not Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User) and
            not Parent.IsOnCooldown(ScriptName, ScriptSettings.Command) and
            Parent.HasPermission(data.User, ScriptSettings.Permission, "instant-replay")):
            UpdateInstantReplayRequestCount()
            Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.UserCooldown)  # Put the command on cooldown

    return

#---------------------------
# Tick method
#---------------------------
def Tick():
    return

#---------------------------
# Parse method
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString

#---------------------------
# Reload Settings
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)

    # Parse hotkey
    UserHotkey = ParseUserHotkey(ScriptSettings.Hotkey)

    return

#---------------------------
# Unload
#---------------------------
def Unload():
    return

#---------------------------
# ScriptToggled
#---------------------------
def ScriptToggled(state):
    return

#---------------------------
# UpdateInstantReplayRequestCount (Manages instant-replay behavior)
#---------------------------
def UpdateInstantReplayRequestCount():
    """ Saves a replay and switches scenes for a set duration when a threshold is reached. """
    global InstantReplayRequestCount
    global MostRecentRequest
    global UserHotkey

    # Brand new window of requests
    if InstantReplayRequestCount == 0:
        # Save replay buffer
        SaveReplay()

    # Reset request count if too few requests within window, start new set of requests
    window = datetime.now() - MostRecentRequest
    if window.total_seconds() > ScriptSettings.UserCooldown:
        InstantReplayRequestCount = 1
        # Save replay buffer
        SaveReplay()
    else:
        InstantReplayRequestCount += 1

    # Have enough people requested a replay?
    if InstantReplayRequestCount >= ScriptSettings.Threshold:
        # Reset instant replay
        InstantReplayRequestCount = 0
        #Parent.SendStreamMessage("Here comes the instant replay!")

        # Switch to the instant replay OBS scene
        # Wait for ReplayDuration (2 second buffer time for transitions, adjust accordingly)
        # Return to the original OBS scene
        Parent.AddCooldown(ScriptName, ScriptSettings.Command, ScriptSettings.Cooldown)
        ChangeSceneTimed(ScriptSettings.InstantReplayScene, int(ScriptSettings.ReplayDuration - 2), ScriptSettings.BaseScene)

    MostRecentRequest = datetime.now()
    return

#---------------------------
# ParseUserHotkey (Maps the user's hotkey to a Virtual Key)
#---------------------------
def ParseUserHotkey(hotkey):
    """ Converts user hotkey string into a virtual key. """
    # Default hotkey is F12
    if hotkey in VK.symbol:
        return VK.symbol.get(hotkey)
    else:
        return getattr(VK, hotkey.replace(' ', '_').lower(), VK.f12)

#---------------------------
# SaveReplay (Press the UserHotkey and wait for the replay to save)
#---------------------------
def SaveReplay(delay = 5, alert = ScriptSettings.AlertChat):
    """ Saves instant replay and alerts chat as needed. """
    StrikeKey(UserHotkey)
    time.sleep(delay)

    if alert:
        Parent.SendStreamMessage("Need " + str(int(ScriptSettings.Threshold)) + " chatters to send " + ScriptSettings.Command + " to show an instant replay.")


#---------------------------------------
# SLOBS Functions - created by ocgineer
#---------------------------------------
def Logger(response):
    """ Logs response from bridge app in scripts logger. """
    if response:
        Parent.Log(ScriptName, response)
    return

def ChangeScene(scene, delay=None):
    """ Change to scene. """
    if delay:
        Logger(os.popen("{0} change_scene \"{1}\" {2}".format(BridgeApp, scene, delay)).read())
    else:
        Logger(os.popen("{0} change_scene \"{1}\"".format(BridgeApp, scene)).read())
    return

def ChangeSceneTimed(scene, delay, returnscene=None):
    """ Swap to scene and then back or to optional given scene. """
    if returnscene:
        Logger(os.popen("{0} swap_scenes \"{1}\" {2} \"{3}\"".format(BridgeApp, scene, delay, returnscene)).read())
    else:
        Logger(os.popen("{0} swap_scenes \"{1}\" {2}".format(BridgeApp, scene, delay)).read())
    return

def SetSourceVisibility(source, visibility, scene=None):
    """ Set the visibility of a source optionally in a targeted scene. """
    if scene:
        Logger(os.popen("{0} visibility_source_scene \"{1}\" \"{2}\" {3}".format(BridgeApp, source, scene, visibility)).read())
    else:
        Logger(os.popen("{0} visibility_source_active \"{1}\" {2}".format(BridgeApp, source, visibility)).read())
    return

def SetSourceVisibilityTimed(source, mode, delay, scene=None):
    """ Set the visibility of a source timed optionally in a targeted scene. """
    if scene:
        Logger(os.popen("{0} tvisibility_source_scene \"{1}\" \"{2}\" {3} {4}".format(BridgeApp, source, scene, delay, mode)).read())
    else:
        Logger(os.popen("{0} tvisibility_source_active \"{1}\" {2} {3}".format(BridgeApp, source, delay, mode)).read())
    return

def SetFolderVisibility(folder, visibility, scene=None):
    """ Set the visibility of a folder optinally in a targeted scene. """
    Parent.Log("functest", "{0} and {1} on {2}".format(folder, visibility, scene))
    if scene:
        Logger(os.popen("{0} visibility_folder_scene \"{1}\" \"{2}\" {3}".format(BridgeApp, folder, scene, visibility)).read())
    else:
        Logger(os.popen("{0} visibility_folder_active \"{1}\" {2}".format(BridgeApp, folder, visibility)).read())
    return

def SetFolderVisibilityTimed(folder, mode, delay, scene=None):
    """ Set the visibility of a folder timed optionally in a targeted scene. """
    if scene:
        Logger(os.popen("{0} tvisibility_folder_scene \"{1}\" \"{2}\" {3} {4}".format(BridgeApp, folder, scene, delay, mode)).read())
    else:
        Logger(os.popen("{0} tvisibility_folder_active \"{1}\" {2} {3}".format(BridgeApp, folder, delay, mode)).read())
    return

def SaveReplaySwap(scene, offset=None):
    """ Save the replay and swap to a given "replay" scene. """
    if offset:
        Logger(os.popen("{0} save_replaybuffer_swap \"{1}\" {2}".format(BridgeApp, scene, offset)).read())
    else:
        Logger(os.popen("{0} save_replaybuffer_swap \"{1}\"".format(BridgeApp, scene)).read())
    return

def ThreadedFunction(command):
    Logger(os.popen("{0} {1}".format(BridgeApp, command)).read())
    return
