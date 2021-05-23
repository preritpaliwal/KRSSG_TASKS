# import gym
# env = gym.make("pendulum-v0")

# while True:
#     obs = env.reset()
#     done = False
#     while not done:
#         action = env.action_space.sample()
#         obs,rew,done,misc = env.step(action)
        # env.render()

# import gym
# env = gym.make('CartPole-v0')
# env.reset()
# for _ in range(1000):
#     env.render()
#     env.step(env.action_space.sample()) # take a random action
# env.close()


# import gym
# env = gym.make('CartPole-v0')
# for i_episode in range(20):
#     observation = env.reset()
#     for t in range(100):
#         env.render()
#         print(observation)
#         action = env.action_space.sample()
#         observation, reward, done, info = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break
# env.close()



# import gym
# env = gym.make('CartPole-v0')
# print(env.action_space)
# #> Discrete(2)
# print(env.observation_space)

# print(env.observation_space.high)
# #> array([ 2.4       ,         inf,  0.20943951,         inf])
# print(env.observation_space.low)
# #> array([-2.4       ,        -inf, -0.20943951,        -inf])



# from gym import spaces
# space = spaces.Discrete(8) # Set with 8 elements {0, 1, 2, ..., 7}
# x = space.sample()
# print(space.contains(x))
# assert space.n == 8

import gym

env_name = "Pendulum-v0"
env = gym.make(env_name)
env2 = gym.make("CartPole-v0")
print(type(env.action_space))
print(type(env2.action_space))