#!/usr/bin/python3
import sys
import os
import getpass
import grp
import argparse
import json
from pathlib import Path


def check_plugdev():
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
    parser = argparse.ArgumentParser()

    # options
    parser.add_argument('--s')

    # hex for single
    parser.add_argument('--h')

    # twin hex
    parser.add_argument('--tl')
    parser.add_argument('--tr')

    args = parser.parse_args()

    self.scheme = args.s
    self.hex = args.h

    self.twin_l = args.tl
    self.twin_r = args.tr

    device_manager = rclient.DeviceManager()
    self.devlist = []
    for device in device_manager.devices:
      self.devlist.append(device)
    self.set_scheme()


  # options
  # single
  # twin
  # {custom}

  def set_scheme(self):
    for device in self.devlist:
      try:
        if device.type == 'keyboard':
          if not self.scheme:
            self.set_default(device)
          elif self.scheme == 'single':
            if not self.hex:
              print('provide a color in hex format by appending --h')
              exit(1)
            self.set_single(device)
          elif self.scheme == 'twin':
            if not self.twin_l or not self.twin_r:
              print('provide two colors hex --tl, --tr')
              exit(1)
            self.set_twin(device)
          else:
            self.set_custom(device)
      except Exception as e:
        print(e)
        pass
  
  def set_default(self, device):
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

  def set_single(self, device):
    h = self.hex.lstrip('#')
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    row = 0
    for _i in range(krow):
      col = 1
      for _ii in range(kcol):
        device.fx.advanced.matrix.set(row, col, rgb)
        if (col >= kcol):
          col = 1
          continue
        col += 1
      row += 1
    device.fx.advanced.draw()

  
  def set_custom(self, device):
    schemes_path = 'schemes'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
      with open('%s/%s/%s.json' % (ROOT_DIR, schemes_path, self.scheme)) as f:
        scheme_file = json.load(f)
        for i in scheme_file['layout']:
          if i['key'] == 'blank':
            continue
          device.fx.advanced.matrix.set(i['row'], i['col'], (i['r'], i['g'], i['b']))
      device.fx.advanced.draw()
    except FileNotFoundError:
      print('scheme file not found')
      return
    
  def set_twin(self, device):
    l_hex = self.twin_l.lstrip('#')
    r_hex = self.twin_r.lstrip('#')

    l_rgb = tuple(int(l_hex[i:i+2], 16) for i in (0, 2, 4))
    r_rgb = tuple(int(r_hex[i:i+2], 16) for i in (0, 2, 4))

    l = {
      "r": l_rgb[0],
      "g": l_rgb[1],
      "b": l_rgb[2],
    }

    r = {
      "r": r_rgb[0],
      "g": r_rgb[1],
      "b": r_rgb[2],
    }

    rdiff = abs(l['r'] - r['r'])
    gdiff = abs(l['g'] - r['g'])
    bdiff = abs(l['b'] - r['b'])

    rdiff_row_q = rdiff / kcol
    gdiff_row_q = gdiff / kcol
    bdiff_row_q = bdiff / kcol

    gradient_list = []

    for i in range(kcol):
      gradient_list.append((l["r"], l["g"], l["b"]))
  
      # r
      if l['r'] < r['r']:
        l['r'] = int(round(l['r'] + rdiff_row_q))
      else:
        l['r'] = int(round(l['r'] - rdiff_row_q))

      # g
      if l['g'] < r['g']:
        l['g'] = int(round(l['g'] + gdiff_row_q))
      else:
        l['g'] = int(round(l['g'] - gdiff_row_q))

      # b
      if l['b'] < r['b']:
        l['b'] = int(round(l['b'] + bdiff_row_q))
      else:
        l['b'] = int(round(l['b'] - bdiff_row_q))

    for _i in range(krow):
      for _ii in range(kcol):
        device.fx.advanced.matrix.set(_i, _ii + 1, gradient_list[_ii])

    device.fx.advanced.draw()

# initialize this shit
StaticColors()
