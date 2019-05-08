#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
PS4 Controller pygame link

'''

import os
import pprint
import pygame

def ds_to_tello(kind, key, value):
    if kind == 'axis':
        if key == 0:
            if value < 0:
                return 'left 20'
            return 'right 20'
        if key == 1:
            if value < 0:
                return 'forward 20'
            return 'backward 20'
        if key == 3:
            if value < 0:
                return 'ccw 20'
            return 'cw 20'
        if key == 4:
            if value < 0:
                return 'up 20'
            return 'down 20'
    if kind == 'button_down':
        if key == 0: # x 
            return 'land'
        if key == 2: # triangle
            return 'takeoff'
        if key == 4: # L1
            return 'flip l'
        if key == 5: # R1
            return 'flip r'
        if key == 8:
            return 'streamon'
        if key == 9:
            return 'streamoff'
        if key == 10:
            return 'emergency'


class PS4Controller(object):
    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def event_to_tello(event):
        if event.type == pygame.JOYAXISMOTION:
            self.axis_data[event.axis] = round(event.value, 2)
            return ds_to_tello('axis', event.axis, round(event.value, 2)) 
        elif event.type == pygame.JOYBUTTONDOWN:
            self.button_data[event.button] = True
            return ds_to_tello('button_down', event.button, None)
            # kind, data = 'button_down', self.button_data
        elif event.type == pygame.JOYBUTTONUP:
            self.button_data[event.button] = False
            # kind, data = 'button_up', self.button_data
        elif event.type == pygame.JOYHATMOTION:
            self.hat_data[event.hat] = event.value
            # kind, data = 'hat', self.hat_data
        return None


    def get_controls():
        return [self.event_to_tello(e) for e is pygame.event.get() if e]

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            ret = []
            for event in pygame.event.get():
                cmd = None
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                    cmd = ds_to_tello('axis', event.axis, round(event.value, 2)) 
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                    cmd = ds_to_tello('button_down', event.button, None)
                    # kind, data = 'button_down', self.button_data
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                    # kind, data = 'button_up', self.button_data
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value
                    # kind, data = 'hat', self.hat_data
                if cmd:
                    ret.append(cmd)
            return ret
                # os.system('clear')
                # pprint.pprint(self.button_data)
                # pprint.pprint(self.axis_data)
                # pprint.pprint(self.hat_data)


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
