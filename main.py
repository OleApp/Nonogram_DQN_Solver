
from NonogramEnv import NonogramEnv
from QLearning import Agent
import torch

env = NonogramEnv(5, 5)

agent = Agent(state_size=64, action_size=env.action_space.n, seed=0)

agent.qnetwork_local.load_state_dict(torch.load('trained_model.pth'))

state = env.reset()


for i in range(100):
    action = agent.act(state)

    state, reward, done, _ = env.step(action)
    print(i, action, reward, done)
    if done:
        print("SOLVED!")
        env.render()
        break

env.render()