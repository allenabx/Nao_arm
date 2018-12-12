# @Author   : Chen Mingyang
# @Time     : 2018/11/20
# @FileName : train.py

from DQN import DQN
from Env import Env
import numpy as np
from params import *
import torch

dqn = DQN()

cnt,distance = 0,99999
for i_episode in range(EPISODE):
    TARGET = np.array(getPos(randAng()))
    env = Env(TARGET)
    curr_state = env.reset()
    ep_r,stp = 0, 0
    while True:
        action = dqn.choose_action(curr_state)
        next_state, reward, done = env.step(action)
        dqn.store_transition(curr_state, action, reward, next_state)
        # print(curr_state, action, reward, next_state)
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
            break


    if i_episode % 10 == 0:
        print('Ep: ', i_episode,
              '| Ep_r: ', round(ep_r, 2),
              '| min_distance: ',  distance,
              '|cnt = ',cnt)
        distance = 999999
        cnt = 0


torch.save(dqn.eval_net, 'eval_net.pkl')
torch.save(dqn.target_net, 'target_net.pkl')
