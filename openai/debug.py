import numpy as np
all_gradients=np.load('all_gradients.npy').tolist()
all_rewards = np.load('all_rewards.npy').tolist()


for var_index in range(4):
    import pdb;pdb.set_trace()
    a=[reward * all_gradients[game_index][step][var_index] for game_index,rewards in enumerate(all_rewards) for step,reward in enumerate(rewards)]
    
