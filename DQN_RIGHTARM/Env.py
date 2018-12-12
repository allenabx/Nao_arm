# @Author   : Chen Mingyang
# @Time     : 2018/11/20
# @FileName : Env.py

import ctypes
import math
import numpy as np
import torch
from params import *


class Env(object):
    """The simulation environment of Nao

    Attributes:
        target      : Final target position, numpy array with dim (3, ), like [1., 2., 3.]
        angles      : Angles of all joint of nao
        num_angles  : Number of angles
        arm0        : Index of right shoulder in angles
        lib         : C++ .so library
        num_step    : Number of steps
    """
    def __init__(self, target: 'np array'):
        """
        Param:
            target: final target position, numpy array with dim (3, ), like [1., 2., 3.]
        """
        self.target = target
        self.arm0 = 18
        self.num_angles = 24
        self.angles = (ctypes.c_float * self.num_angles)()
        self.num_step = 0
        # load c++ library as lib
        self.lib = ctypes.cdll.LoadLibrary('../release/base.so')
        self.init_angles()

    def init_angles(self):
        for i in range(self.num_angles):
            self.angles[i] = 0

    def if_done(self, state):
        """

        Return:
            [True/False, comment], return True if step done and have comments;
            comment == 'Limit'  : done because of angles out of limits
            comment == 'Target' : done because of being around target
        """
        # limit the angles of right arm joint and detect if around target

        if (-120.0 > self.rad2ang(self.angles[self.arm0 + 0]) or self.rad2ang(self.angles[self.arm0 + 0]) > 120.0
                or -95.0 > self.rad2ang(self.angles[self.arm0 + 1]) or self.rad2ang(self.angles[self.arm0 + 1]) > 1.0
                or -120.0 > self.rad2ang(self.angles[self.arm0 + 2]) or self.rad2ang(self.angles[self.arm0 + 2]) > 120.0
                or -1.0 > self.rad2ang(self.angles[self.arm0 + 3]) or self.rad2ang(self.angles[self.arm0 + 3]) > 90.0):
            return [True, "Limit"]
        # precision

        elif np.linalg.norm(self.target - state[0:3].numpy()) < PRECISION:
            return [True, "Target"]
        else:
            return [False, None]

    def fix(self):
        if(-120.0 > self.rad2ang(self.angles[self.arm0 + 0])):
            self.angles[self.arm0 + 0] += self.ang2rad(ACTIONS_Per_JOINT[1])
        elif(self.rad2ang(self.angles[self.arm0 + 0]) > 120.0):
            self.angles[self.arm0 + 0] += self.ang2rad(ACTIONS_Per_JOINT[0])
        if(-95.0 > self.rad2ang(self.angles[self.arm0 + 1])):
            self.angles[self.arm0 + 1] += self.ang2rad(ACTIONS_Per_JOINT[1])
        elif(self.rad2ang(self.angles[self.arm0 + 1]) > 1.0):
            self.angles[self.arm0 + 1] += self.ang2rad(ACTIONS_Per_JOINT[0])
        if(-120.0 > self.rad2ang(self.angles[self.arm0 + 2])):
            self.angles[self.arm0 + 2] += self.ang2rad(ACTIONS_Per_JOINT[1])
        elif(self.rad2ang(self.angles[self.arm0 + 2]) > 120.0):
            self.angles[self.arm0 + 2] += self.ang2rad(ACTIONS_Per_JOINT[0])
        if(-1.0 > self.rad2ang(self.angles[self.arm0 + 3])):
            self.angles[self.arm0 + 3] += self.ang2rad(ACTIONS_Per_JOINT[1])
        elif(self.rad2ang(self.angles[self.arm0 + 3]) > 90.0):
            self.angles[self.arm0 + 3] += self.ang2rad(ACTIONS_Per_JOINT[0])

    def reset(self):
        self.init_angles()

        return self.get_state()

    def action_map(self, action_num):
        """Map action number to action like [Joint, Angle]"""
        aux = ACTIONS_Per_JOINT
        assert len(aux) == N_ACTIONS_Per_JOINT
        return [action_num // N_ACTIONS_Per_JOINT, aux[action_num % N_ACTIONS_Per_JOINT]]

    def step(self, action_num):
        """Do given action

        Params:
            action_num: Number of action current and should be mapped to action like [Joint, Angle], Joint \in [0, 1, 2, 3], Angle \in [-1, 0, 1]
        Return:
            next_state: Next state(position) after this action, state'e type is torch.FloatTensor with dim (3, )
            reward    : Reward of current state
            done      : Done will be True if action makes angles out of limits
        """
        # do action and get next state
        action_j, action_a = self.action_map(action_num)
        self.angles[self.arm0 + action_j] += self.ang2rad(action_a)
        self.fix()
        next_state = self.get_state()
        # get reward
        reward = self.get_reward(next_state)
        # if done
        # TODO curr_state or next_state?
        done = self.if_done(next_state)

        self.num_step += 1
        return next_state, reward, done

    def ang2rad(self, ang):
        """Map angle to radian"""
        return math.pi / 180 * ang

    def rad2ang(self, rad):
        """Map radian to angle"""
        return 180 / math.pi * rad

    def get_reward(self, s):
        """Define the reward here"""
        if self.if_done(s)[1] == 'Limit':
            r = -1000
        elif self.if_done(s)[1] == 'Target':
            r = 1000
        else:
            r =  -np.linalg.norm(self.target - s.numpy()[0:3])/100
            # r = 0
        return r

    def get_state(self):
        """Get current state by current angles

        Return:
            The state wrapped by torch.FloatTensor with dim (3, )
        """
        # declare the return type of Kinematics
        class Pos(ctypes.Structure):
            _fields_ = [
                ("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("z", ctypes.c_float)
            ]
        self.lib.Kinematics.restype = Pos

        angel_list = []

        for i in range(N_JOINTS):https://github.com/allenabx/Nao_arm_2/blob/master/1234.py
            angel_list.append(self.rad2ang(self.angles[self.arm0 + i]))


        pos = self.lib.Kinematics(self.angles)

        angel_list[0:0] = self.target[:]
        angel_list[0:0] = [pos.x, pos.y, pos.z]

        return torch.tensor(angel_list).type(torch.FloatTensor)

