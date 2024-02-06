import gym
import matplotlib.pyplot as plt


# Create the Blackjack environment
env = gym.make("Blackjack-v1", render_mode="human")

# Initialize the game
state = env.reset()
done = False

# Loop through the game until it's finished
while not done:
    
    # Print the current state of the game
    print(f"Current state: {state}")

    # Choose an action (hit or stick)
    action = env.action_space.sample()
    print(f"Taking action: {action}")

    # Take the action and observe the result
    next_state, reward, done, n, _ = env.step(action)
    
    # Print the next state of the game
    print(f"Next state: {next_state}")

    # Update the state
    state = next_state

# The game is finished, so close the window
env.close()