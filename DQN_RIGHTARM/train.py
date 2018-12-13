# @Author   : Chen Mingyang
# @Time     : 2018/11/20
# @FileName : train.py

from DQN import DQN
from Env import Env
import numpy as np
from params import *
import torch
import matplotlib.pyplot as plt

dqn = DQN()


cnt,distance = 0,99999
dis = []
TARGET = np.array(getPos(randAng()))
env = Env(TARGET)
for i_episode in range(EPISODE):

    curr_state = env.reset()
    ep_r,stp = 0, 0
    while True:
        action = dqn.choose_action(curr_state)
        next_state, reward, done = env.step(action)
        dqn.store_transition(curr_state, action, reward, next_state)

        ep_r += reward

        curr_state = next_state
        stp += 1
        if (np.linalg.norm(TARGET - curr_state.numpy()[0:3])) < distance :
            distance  =  np.linalg.norm(TARGET - curr_state.numpy()[0:3])


        if dqn.memory_counter > MEMORY_CAPACITY:
            dqn.learn()
        if done[1] == 'Target':
            cnt += 1
        if done[0] or stp > MAX_STEP:
            dis.append(np.linalg.norm(TARGET - curr_state.numpy()[0:3]))
            break

    if i_episode % 10 == 0:
        print('Ep: ', i_episode,
              '| Ep_r: ', round(ep_r, 2),
              '| min_distance: ',  distance,
              '|cnt = ',cnt)
        distance = 999999
        cnt = 0

        y = dis
        x = range(len(y))  # 以0开始的递增序列作为x轴数据
        plt.plot(x, y)  # 只提供x轴，y轴参数，画最简单图形
        plt.show()
    if i_episode % 100 == 0 :
        y = dqn.plt_loss  # 设置y轴数据，以数组形式提供
        x = range(len(y))  # 以0开始的递增序列作为x轴数据
        plt.plot(x, y)  # 只提供x轴，y轴参数，画最简单图形
        plt.show()

torch.save(dqn.eval_net, 'eval_net.pkl')
torch.save(dqn.target_net, 'target_net.pkl')
