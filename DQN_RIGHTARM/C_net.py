"""useing to connect 3D simulation"""

from DQN import DQN
from Env import *
import numpy as np

import time
import ctypes
import math

class Cnet():
    def __init__(self, ):
        self.dqn = DQN()
        self.dqn.eval_net = torch.load('./eval_net.pkl')
        self.dqn.target_net = torch.load('./target_net.pkl')
        self.num_angles = 24
        self.angles = (ctypes.c_float * self.num_angles)()
        self.lib = ctypes.cdll.LoadLibrary('../release/base.so')

        self.TARGET = np.array(getPos(randAng()))
        self.arm0 = 18
    # load c++ library as lib

    def get_state(self,angles):
        """Get current state by current angles

        Return:
            The state wrapped by torch.FloatTensor with dim (3, )
        """
        # declare the return type of Kinematics

        for i in range(24):
            self.angles[i] = self.ang2rad(angles[i])

        class Pos(ctypes.Structure):
            _fields_ = [
                ("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("z", ctypes.c_float),
                ("elbowx", ctypes.c_float),
                ("elbowy", ctypes.c_float),
                ("elbowz", ctypes.c_float)
            ]
        self.lib.Kinematics.restype = Pos

        state = []

        pos = self.lib.Kinematics(self.angles)

        state[0:0] = self.TARGET[:]
        state[0:0] = [pos.x, pos.y, pos.z, pos.elbowx, pos.elbowy, pos.elbowz]

        return torch.tensor(state).type(torch.FloatTensor)

    def choose_action_C(self,angels):
        curr_state = self.get_state(angels)

        print(np.linalg.norm(self.TARGET - curr_state.numpy()[0:3]))
        action = cnet.dqn.choose_action(curr_state)

        action_j, action_a = self.action_map(action)

        self.angles[self.arm0 + action_j] += self.ang2rad(action_a)

        return self.rad2ang_array(self.ctype2np(self.angles))

    def action_map(self, action_num):
        """Map action number to action like [Joint, Angle]"""
        aux = ACTIONS_Per_JOINT
        assert len(aux) == N_ACTIONS_Per_JOINT
        return [action_num // N_ACTIONS_Per_JOINT, aux[action_num % N_ACTIONS_Per_JOINT]]

    def ang2rad(self, ang):
        """Map angle to radian"""
        return math.pi / 180 * ang

    def rad2ang(self, rad):
        """Map radian to angle"""
        return 180 / math.pi * rad

    def ctype2np(self,ctype):
        np = []
        for i in range(len(ctype)):
            np.append(ctype[i])
        return np

    def rad2ang_array(self,rads):
        array = []
        for i in range(len(rads)):
            array.append(180 / math.pi * rads[i])
        return array
    
cnet = Cnet()
state = np.zeros(24)
state = cnet.choose_action_C(state)
while True:
    state = cnet.choose_action_C(state)

#ssss
# cnet = Cnet()
# temp = np.zeros( 24 )
# temp2 = cnet.choose_action_C(temp)
# for i in range(24):
#     temp[i] = temp2[i]
# print(temp)
#
# env = Env(cnet.TARGET)
# curr_state = env.reset()
# print(curr_state)
# stp = 0
# while True:
#     action = cnet.dqn.choose_action(curr_state)
#     print(action)
#     next_state, reward, done = env.step(action)
#     stp += 1
#
#     if done[0]:
#         print(stp)
#         break
#     curr_state = next_state
#     time.sleep(0.1)
#     distance = np.linalg.norm(cnet.TARGET - curr_state.numpy()[0:3])
#     print(distance)
