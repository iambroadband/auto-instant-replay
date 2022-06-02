# auto-instant-replay

<sub><sup>This is a Python script meant for use with [Streamlabs Chatbot](https://streamlabs.com/content-hub/support/chatbot-and-cloudbot).</sup></sub>
### Author: iBroadband
##### Script Version: 1.0.8


## Where to Find Me
| What?   |                         Where?                            |
| ------- | --------------------------------------------------------- |
| E-Mail  | [iambroadband@gmail.com](mailto:iambroadband@gmail.com)   |
| Discord | [Broadband#9214](https://www.discord.gg/Broadband)        |
| Twitch  | [iBroadband](https://www.twitch.tv/iBroadband)            |
| Twitter | [@iambroadband](https://www.twitter.com/iambroadband)     |
| Youtube | [Broadband](https://www.youtube.com/channel/UC6xvUC5NThwShk-wrhh01Mg) |
| Github  | [Broadband](https://github.com/broadband)                 |


## What Can It Do?
You'll want to use this script if you are looking for a way to allow your viewers to request instant replays from your chat. This script will listen to chat and wait for the number of requests to exceed your set threshold within a set window of time (30s). When it does, it will automatically change your OBS scene for the duration of your replay then return to the original scene.


## Installation
1. Download as [a .ZIP](https://github.com/iBroadband/auto-instant-replay/archive/refs/heads/main.zip)
2. Extract to your local scripts folder (e.g. `C:\Users\iBroadband\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts`)
3. Open Streamlabs Chatbot and go to the Scripts tab. `Right Click > Reload Scripts`


## Setup
1. Set up an instant replay scene on OBS. [Here is a good resource](https://youtu.be/7fi7RI4y_6o) from Defrag on Youtube.
2. Make sure you have a hotkey assigned that switches to your replay scene.
3. In `Script Settings > OBS Settings` update the following:
    - `OBS Replay Hotkey`
    - `Base Scene`
    - `Instant Replay Scene`
    - `Replay Duration`
4. The default settings will work out of the box for the rest. Adjust them as needed.


## Settings
### Basic Settings
###### The most basic settings
---
##### Command
The chat command your viewers can use to request a replay.
- **default**: `!replay`

##### Alert Chat
True/False flag for informing chat about the status of the request.
- **default**: `True` (bot will update chat with request count and threshold)
- `False` (bot will not update chat)

##### Command Cooldown
How long before this command is allowed to request a replay again?
- **default**: 60 seconds
<br />

### OBS Settings
###### Settings related to (SL)OBS and your scenes
---
##### OBS Replay Hotkey
The hotkey you use to switch to your instant replay scene in OBS.
- e.g.: `F12`, `Home`, `Backspace`, `Esc`, `Caps Lock`, `a`, `num 1`, `Left Shift`
- Features support for [~all~ most MSDN virtual keys](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes). Case insensitive.
- **default**: F12

##### Base Scene
The name of the scene you want to switch from.
- **default**: In Game
- Case sensitive!

##### Instant Replay Scene
The name of the scene that you want to switch to.
- **default**: In Game (Replay Display)
- Case sensitive!

##### Replay Duration
The duration of your instant replay buffer in seconds.
- **default**: 30 seconds
- There is a built in buffer time of 2 seconds for transitions. As a result, setting this duration to less than 2 seconds may not work.
<br />

### Viewer Settings
###### Settings related to viewer permissions and trigger conditions
---
##### Permission<br />
Determines who has access to requesting a replay from chat.
- **default**: everyone
- moderator
- subscriber
- user_specific
- editor

##### Trigger Threshold<br />
How many users need to request a replay within 30 second window to trigger a replay?
- **default**: 3

##### User Cooldown<br />
How long before an individual user is allowed to request a replay again?
- **default**: 60 seconds


## Known Issues
none, it's perfect 😎

- Planned improvement: add a setting for window size in case users want shorter or longer windows to allow for requests.


If you're a developer, feel free to fork this repo or make a pull request. <br />
If you're not a developer, but you find a problem or have a feature request, please contact me!


## Resources
- [Streamlabs Chatbot Features](https://cdn.streamlabs.com/chatbot/Documentation_Twitch.pdf)
- [Streamlabs Chatbot Python Boilerplate](https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate)
- 🧠


## Contact
Please email me or DM me on Discord or Twitter if you have questions, concerns, bug reports, or feature requests.
