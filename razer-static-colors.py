#!/usr/bin/python3
import sys
import os
import getpass
import grp


def check_plugdev():
  """Check if group 'plugdev' exists and current user is its member.
  If razerCommander is being run from within a flatpak, skip this check.
  There is apparently no way to check groups with flatpak confinement."""
  if os.path.isfile('{}/flatpak-info'.format(os.environ['XDG_RUNTIME_DIR'])):
    return
  try:
    if not getpass.getuser() in grp.getgrnam('plugdev').gr_mem:
      print('''
ERROR: you are not part of the plugdev group. Add yourself to it:
  $ sudo gpasswd -a <YOUR_USERNAME> plugdev
''')
      exit(1)
  except KeyError:
    print('''
ERROR: the plugdev group doesn\'t exist. Make sure you installed the openrazer
driver, in case you did, create the plugdev group and add yourself to it:
  $ sudo groupadd plugdev
  $ sudo gpasswd -a <YOUR_USERNAME> plugdev
''')
    exit(1)


check_plugdev()

import openrazer.client as rclient

# this is for standard TKL layout (e.g. Huntsman Tournament Edition TKL) change this based on your Razer keyboard layout
# you can also change the code structure/ implementation by whatever you want
krow = 6
kcol = 17

colors = [
  (255, 255, 0),      # yellow
  (0, 255, 0),        # green
  (0, 255, 255),      # cyan
  (0, 0, 255),        # blue
  (255, 0, 255),      # magenta
  (255, 0, 0),        # red
  (255, 128, 0),      # orange
]

class StaticColors:
  def __init__(self):
    device_manager = rclient.DeviceManager()
    self.devlist = []
    for device in device_manager.devices:
      self.devlist.append(device)
    self.initDevices()

  def initDevices(self):
    for device in self.devlist:
      try:
        if device.type == 'keyboard':
          self.colorize(device)
      except:
        pass
  
  def colorize(self, device):
    row = 0
    color_group_index = 0
    for _i in range(krow):
      col = 1
      for _ii in range(kcol):
        device.fx.advanced.matrix.set(row, col, colors[color_group_index])
        if (color_group_index + 1) == len(colors):
          color_group_index = 0
        else:
          color_group_index += 1
        if (col >= kcol):
          col = 1
          continue
        col += 1
      row += 1
    device.fx.advanced.draw()

StaticColors()
