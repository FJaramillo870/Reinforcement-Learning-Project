#First we're importing all the libraries
import numpy as np
import gymnasium as gym
import random
import time
from IPython.display import clear_output
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#Next, to create our environment, we just call gym.make()
#and pass a string of the name of the environment we want to set up.
env = gym.make('FrozenLake-v1', render_mode='ansi', is_slippery=False)
#Creating the action space, which is responsible for The Space object corresponding to valid actions,
#all valid actions should be contained within the space.
action_space_size = env.action_space.n
#The Space object corresponding to valid observations, all valid observations should be contained within the space.
#Observations refer to the information that an agent receives from the environment.
#In the context of reinforcement learning, observations are typically used to capture the current state or
#partial information about the state of the environment.
state_space_size = env.observation_space.n
#We're now going to construct our Q-table, and initialize all the Q-values to zero for each state-action pair.
q_table = np.zeros((state_space_size, action_space_size))

print(q_table)


#Now, we're going to create and initialize all the parameters needed to implement the Q-learning algorithm.
#The number of episodes we are using train our agent. Episodes are
#Number of total episodes we used to train our model
num_episodes = 10000
#total number of moves or agent can make before it is ended
max_steps_per_episode = 100

learning_rate = 0.1
discount_rate = 0.99

#The rate resposible for the movement of our agent on the gameboard
exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.01

#We create this list to hold all of the rewards we'll get from each episode.
#This will be so we can see how our game score changes over time.
rewards_all_episodes = []

#In the following block of code, we'll implement the entire Q-learning algorithm
#When this code is executed, this is exactly where the training will take place.
#This first for-loop contains everything that happens within a single episode.
#This second nested loop contains everything that happens for a single time-step.
for episode in range(num_episodes):
    #preps envirnment to run
    state = env.reset()[0]
    #keeps track of whether the episode finished or not
    done = False
    #Keeps track of rewards from the current episode
    rewards_current_episode = 0

    #we set our exploration_rate_threshold to a random number between 0 and 1.
    #This will be used to determine whether our agent will explore or exploit the environment in this time-step
    for step in range(max_steps_per_episode):
        # Exploration-exploitation trade-off
        exploration_rate_threshold = random.uniform(0, 1)
        #our agent will exploit the environment and choose the action that has the
        #highest Q-value in the Q-table for the current state
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state, :])
        #the threshold is less than or equal to the exploration_rate,
        #then the agent will explore the environment, and sample an action randomly.
        else:
            action = env.action_space.sample()

        #After the action is chosen this is responsible for taking that action using step()
        new_state, reward, done, truncated, info = env.step(action)

        # Update Q-table for Q(s,a)
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
            learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

        #Transitions to the next state
        state = new_state
        rewards_current_episode += reward

        #check if our last action ended the episode.
        if done == True:
            break

    # Exploration rate decay
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)

    #appends all the rewards from the current episode to list of rewards we made earlier
    rewards_all_episodes.append(rewards_current_episode)


# Calculate and print the average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/1000)
#count = 1000
print(q_table)

variables_to_save = {
    'q_table': q_table,
    'rewards_per_thousand_episodes': rewards_per_thousand_episodes
}
# Save variables to a file
np.save('non_slippery_variables.npy', variables_to_save)

"""
variables_to_save = {
    'q_table': q_table,
    'rewards_per_thousand_episodes': rewards_per_thousand_episodes
}
# Save variables to a file
np.save('is_slippery_variables.npy', variables_to_save)
"""
