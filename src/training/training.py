# import torch

# from src.training.model import Policy
# from src.training.sim import WalkingSim

# EPOCHS = 1000


# def main():
#     sim = WalkingSim()

#     obs = sim.reset()
#     obs_size = len(obs)
#     action_size = len(sim.muscles)

#     policy = Policy(obs_size, action_size)
#     optimizer = torch.optim.Adam(policy.parameters(), lr=3e-4)

#     for episode in range(EPOCHS):
#         obs = sim.reset()
#         total_reward = 0

#         for _ in range(1000):
#             action = policy(obs)
#             obs, reward, done = sim.step(action.detach().numpy())
            
#             total_reward += reward
#             if done:
#                 break
    
#         print(f"[{episode}] Episode reward: {total_reward}")


# if __name__ == "__main__":
#     main()


import torch
import torch.optim as optim
from torch.distributions import Normal

from src.training.model import Policy
from src.training.sim import WalkingSim

import pygame
import pymunk
import pymunk.pygame_util
import matplotlib.pyplot as plt
import numpy as np

CHECKPOINT_VERSION = 5
DO_RENDER = False


def main():
    global DO_RENDER

    if input("Would you like to watch? [y/N]").lower() == "y":
        DO_RENDER = True

    if DO_RENDER:
        pygame.init()

        window = pygame.display.set_mode((1300, 800))

    sim = WalkingSim()

    obs = sim.reset()
    obs_size = len(obs)
    action_size = len(sim.muscles)

    policy = Policy(obs_size, action_size)
    optimizer = optim.Adam(policy.parameters(), lr=3e-4)

    best_reward = float("-inf")
    starting_episode = 0

    try:
        checkpoint = torch.load("walking_model.pt", map_location="cpu")
        if checkpoint.get("version") != CHECKPOINT_VERSION:
            raise ValueError("old checkpoint format")
        policy.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        best_reward = checkpoint["best_reward"]
        starting_episode = checkpoint["episode"]
        print(f"Loaded checkpoint. Episode {starting_episode}, reward: {best_reward}")
    except (FileNotFoundError, ValueError, KeyError, RuntimeError):
        print("Starting a new policy.")
    
    reward_history = []
    
    episode = starting_episode
    try:
        while True:
            obs = sim.reset()
            total_reward = 0

            log_probs = []
            entropies = []
            rewards = []

            for _ in range(sim.max_steps):
                if DO_RENDER:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            plot_rewards(reward_history)
                            return

                obs_tensor = obs

                action_mean = policy(obs_tensor)
                dist = Normal(action_mean, 0.2)
                raw_action = dist.rsample()
                action = torch.tanh(raw_action)
                log_prob = (
                    dist.log_prob(raw_action)
                    - torch.log(1.0 - action.square() + 1e-6)
                ).sum()

                obs, reward, done = sim.step(action.detach().numpy())

                log_probs.append(log_prob)
                entropies.append(dist.entropy().sum())
                rewards.append(reward)
                total_reward += reward

                if done:
                    break
            
                if DO_RENDER:
                    window.fill((0, 0, 0))
                    draw_options = pymunk.pygame_util.DrawOptions(window)
                    sim.space.debug_draw(draw_options)
                    pygame.display.update()

            # Compute returns
            returns = []
            G = 0
            for r in reversed(rewards):
                G = r + 0.99 * G
                returns.insert(0, G)

            returns = torch.tensor(returns, dtype=torch.float32)
            returns = (returns - returns.mean()) / (returns.std() + 1e-8)

            # Policy loss
            policy_loss = torch.stack(
                [-log_prob * G for log_prob, G in zip(log_probs, returns)]
            ).mean()
            entropy_bonus = torch.stack(entropies).mean()
            loss = policy_loss - 0.001 * entropy_bonus

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
            optimizer.step()

            reward_history.append(total_reward)
            print(f"[{episode}] Reward: {total_reward}")

            if total_reward >= best_reward:
                print("Saved checkpoint!")
                torch.save({
                    "version": CHECKPOINT_VERSION,
                    "model_state_dict": policy.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "best_reward": total_reward,
                    "episode": episode
                }, "walking_model.pt")
                best_reward = total_reward
                plot_rewards(reward_history)
            
            if episode % 25 == 0:
                plot_rewards(reward_history)

            if len(reward_history) > 5000:
                reward_history.clear()
            
            episode += 1
    except KeyboardInterrupt:
        plot_rewards(reward_history)
        print("Exiting...")
  


def plot_rewards(rewards, outfile="rewards.png", window=10):
    r = np.array(rewards)

    cumsum = np.cumsum(np.insert(rewards, 0, 0))  # insert 0 to align indices
    rolling_avg = (cumsum[window:] - cumsum[:-window]) / window

    plt.plot(rewards, label="Reward")
    plt.plot(range(window-1, len(rewards)), rolling_avg, label=f"{window}-episode rolling average", color='orange')

    plt.title("Reward over time")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.grid(True)
    plt.legend()
    plt.savefig(outfile)
    plt.close()


if __name__ == "__main__":
    main()
