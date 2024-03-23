# -*- coding: utf-8 -*-
#-----------
# Imports
#-----------
import os
import subprocess
import colors
import socket
from typing import List
from libqtile import qtile, layout, bar, hook, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile.lazy import lazy
#from qtile_extras import widget

#-----------
# User Settings
#-----------

# Colorscheme, referenced by an external colors.py file
# Affects bar, window decorations and widgets inside the said bar
# Available colorschemes: oxocarbon, janleigh, rosepine, radium
colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.oxocarbon()


mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
class Apps:
    terminal = "alacritty"
    launcher = "rofi -show drun"
    browser = "firefox"
    filemanager = "dolphin"
    chatapp = "armcord"
    screenshotter = "flameshot gui"
    lockscreen = "betterlockscreen -l"

class Music:
    next = "mpc --host localhost --port 8800 next"
    prev = "mpc --host localhost --port 8800 prev"
    toggle = "mpc --host localhost --port 8800 toggle"
    volup = "pulsemixer --change-volume +10"
    voldown = "pulsemixer --change-volume -10"
    mute = "pulsemixer --toggle-mute"

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn('alacritty'),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "Return",
             # lazy.spawn("dmenu_run -p 'Run: '"),
             #lazy.spawn("rofi -show drun -show-icons -display-drun \"Run: \" -drun-display-format \"{name}\""),
              lazy.spawn("rofi -show drun -config ~/.config/rofi/config.rasi -display-drun \"Run: \" -drun-display-format \"{name}\""),
             desc='Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "p",
             lazy.spawn("xfce4-power-manager"),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "o",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key([mod, "shift"], "x",
             # lazy.spawn("dmenu_run -p 'Run: '"),
             lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu"),
             desc='power manager'
             ),
         Key([mod, "shift"], "f",
             # lazy.spawn("alacritty -e ranger"),
             lazy.spawn("dolphin"),
             desc='file manager'
             ),
         Key([mod, "shift"], "w",
             lazy.spawn("firefox"),
             desc='web browser'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             )
]

groups = [
        Group("1", layout="monadtall", matches=[Match(wm_class=Apps.browser)]),
        Group("2", layout="monadtall", matches=[Match(wm_class=Apps.chatapp)]),
        Group("3", layout="monadtall", matches=[Match(wm_class=Apps.filemanager)]),
        Group("4", layout="monadtall"),
        Group("5", layout="monadtall"),
        Group("6", layout="max", matches=[Match(wm_class="pcsx2-qt" "prismlauncher")]),
        ]

# This makes our group labels change dynamically,
# Qtile cannot make shapes like in Awesome, so we settle
# for an unicode symbol repeated over for our current group
@hook.subscribe.setgroup
def setgroup():
    for i in range(len(groups)-1):
        qtile.groups[i].label = ""                    #"󰹞"
        qtile.current_group.label = ""                   #""                #"󰹞󰹞󰹞"


# Add group specific keybindings
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Mod + number to move to that group."),
        Key(["mod1"], "Tab", lazy.screen.next_group(), desc="Move to next group."),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group(), desc="Move to previous group."),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="Move focused window to new group."),
    ])

# Define scratchpads
# Refer to your terminal emulator's way to classify sessions,
# wezterm uses 'wezterm start --class' and kitty uses 'kitty --class' for example
groups.append(ScratchPad("scratchpad", [
    DropDown("term", "kitty -T scratch", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown("term2", "kitty -T scratch2", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown("ranger", "kitty -T ranger -e fm", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown("volume", "kitty -T -e alsamixer", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown("mus", "kitty -T -e ncmpcpp", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
]))

# Scratchpad keybindings
keys.extend([
    Key([mod, "shift"], "a", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod, "shift"], "m", lazy.group['scratchpad'].dropdown_toggle('term2')),
    Key([mod], "b", lazy.group['scratchpad'].dropdown_toggle('ranger')),
    Key([mod], "v", lazy.group['scratchpad'].dropdown_toggle('volume')),
    Key([mod, "shift"], "n", lazy.group['scratchpad'].dropdown_toggle('mus')),
])
layout_theme = {"border_width": 3,
                "margin": 10,
                "border_focus": "#282828",                     ##ff6c6b
                "border_normal": "#222222"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Proxima nova Bold ",
    fontsize = 14,
    background="#161616",
    foreground=colors[1],
    border_width=[2, 2, 2, 2],
    border_color=colors[1],
)
extension_defaults = widget_defaults.copy()

def get_widgets():
    widgets = [
        widget.Spacer(length=4),
        widget.TextBox(
            text="",
            foreground="#fff",
            fontsize=20,
            padding=15,
            font="Iosevka Nerd Font",
            ),
        widget.Spacer(length=4),
        widget.GroupBox(
            font="Iosevka Nerd Font",
            highlight_method='text',
            inactive="#2f2f2f",
            active="#ffffff",
            this_current_screen_border="#ffffff",
            urgent_border=colors[0],
            background="#161616",
            padding=2,
            #backgroundColor="#00000000",
            ),
        #widget.TextBox(
         #   text="",
          #  foreground="#000000",
          #  fontsize=23,
           # padding=0,
            #font="Iosevka Nerd Font",
            #),
        widget.Spacer(length=10,
                      background="#161616",), 

        #widget.CurrentLayoutIcon(
        #   use_mask=True,
        #   scale=0.5,
        #   padding=10,
        #   background="#161616",
            # Don't delete this or the bar will go transparent, for some reason
            #$),
        #widget.TextBox(
         #   text="",
          #  foreground="#000000",
           # fontsize=23,
            #padding=0,
            #font="Iosevka Nerd Font",
            #),
        widget.Spacer(),
        widget.TaskList(
            border='#161616',
            urgent_border='#161616',
            font="Proxima nova Bold",
            fontsize=0,
            icon_size=20,
            theme_path='/usr/share/icons/Papirus-Dark/',
            txt_floating=  '🗗',
            txt_maximized =  '🗖',
            txt_minimized =  '🗕',


            ),
        widget.Spacer(),
        widget.Systray(),
        widget.Spacer(length=20,),
    #    widget.OpenWeather(
     #       location='Kandy',
      #      format='{location_city}: {weather_details} {icon}',
       #     json='True',
        #    coordinates='7.2906° N, 80.6337° E',
         #   update_interval="60",
#
 #           ),
      #  widget.TextBox(
       #     text="",
        #    foreground="#000000",
         #   fontsize=23,
          #  padding=0,
           # font="Iosevka Nerd Font",
           # ),
        widget.Wttr(
            location={'Kandy':'Kandy'},
            foreground="#ffffff",
            background="#161616",
            ),
        #widget.TextBox(
         #       text="",
          #      foreground="#000000",
           #     background="#000000",
            #    fontsize=23,
             #   padding=0,
              #  font="Iosevka Nerd Font",
               # ),
        widget.Spacer(
            length= 10,
            background="#161616",
            ),
   #     widget.PulseVolume(
    #            background = "#161616",
     #           foreground = "#fff",
  #              emoji = True,
  #              emoji_list = ['🔇', '🔈', '🔉', '🔊'],
   #             fontsize = 20,
    #            ),
        #widget.TextBox(
         #       text="",
          #      foreground="#000000",
           #     fontsize=23,
            #    padding=0,
             #   font="Iosevka Nerd Font",
              #  ),

        widget.Volume(
            fmt="󰕾 {}",
            mute_command="amixer -D pulse set Master toggle",
            foreground="#ffffff",
            background="#161616",
            padding=0,
            ),
   #     widget.TextBox(
    #            text="",
     #           foreground="#000000",
      #          background="#000000",  
       #         fontsize=23,
        #        padding=0,
         #       font="Iosevka Nerd Font",
          #      ),
        widget.Spacer(length=10,
                      foreground="#000000",
                      background="#161616",
                      ),
#        widget.TextBox(
 #               text="",
  #              foreground="#000000",
   #             fontsize=23,
    #            padding=0,
     #           font="Iosevka Nerd Font",
      #          ),
        widget.Clock(
                format="%I:%M %p",
                foreground="#ffffff",
                background="#161616",
                     ),
     #   widget.TextBox(
      #          text="",
       #         foreground="#000000",
        #        fontsize=23,
         #       padding=0,
          #      ),
        widget.Spacer(length=10),
            ]

    return widgets

screens = [
    Screen(
        top=bar.Bar(
            get_widgets(),
            30,
            margin=4,
            border_color="#282828",
            border_width=0,
            background="#000000",
            opacity=1,
       ),
    ),
]

#-----------
# Mouse
#-----------

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#-----------
# Misc
#-----------

# Which screens spawn as floating by default
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='qview'), 
    Match(wm_class='feh'),
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='flameshot'),
    Match(wm_class='galculator'),
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], fullscreen_border_width = 0, border_width = 0)

# Autostart script, for starting important apps, refer to autostart.sh
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([home])

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
auto_minimize = True
focus_on_window_activation = "smart"
reconfigure_screens = True
wmname = "Qtile"









#window_swallowing


import psutil

@hook.subscribe.client_new
def _swallow(window):
    pid = window.window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()}
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, 'parent'):
        window.parent.minimized = False
