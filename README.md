# Nao-RL

## Installation

1. Install PyTorch

2. Clone the Nao-RL:

   $ git clone [git@github.com:AnselCmy/Nao-RL.git](git@github.com:AnselCmy/Nao-RL.git)

   $ cd Nao-RL

3. Compile C++ files

   $ bash make.sh

## DQN_RIGHTARM

In this part, we do DQN test on right arm of robot **Nao**.

Here is the file tree of this part

```
├── DQN.py
├── Env.py
├── params.py
├── train.py
├── test.py
├── target_net.pkl
└── eval_net.pkl
```

### Quickstart

#### Training

**Step 1:  Set parameters and target** 

All related parameters are in **./DQN_RIGHTARM/params.py**, you can set hyperparameters and others there.

The target value can also be defined there, for example:

```python
TARGET = np.array([197.34, -98.0, 504.68])
```

**Step 2:  Train model**

Using python run **train.py** and finally the main part of DQN will be saved, for example:

```python
torch.save(dqn.eval_net, 'eval_net.pkl')
torch.save(dqn.target_net, 'target_net.pkl')
```

### Testing

For testing the trained model, just run **test.py**, in this model, trained DQN will be loaded and print the action every step.