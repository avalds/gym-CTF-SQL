"""
Copy of a copy: This was copied from https://raw.github.uio.no/fabiomz/gym-qiscoin/master/qiscoin/envs/qiscoin_env.py
Classic cart-pole system implemented by Rich Sutton et al.
Copied from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""

import math,sys
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import matplotlib.pyplot as plt



class CTFSQLEnv0(gym.Env):
	"""
	Description:
		A webserver exposing a query with a potential SQL injection vulnerability. Behind the vulnerability lies a flag.
	Observation:
		Type: MiltiDiscrete(3)
		Num    Observation
		0   action tried and returned a negative answer
		1   action never tried
		2   action tried and returned a positive answer
	Actions:
		Type: Discrete(n)
		Num    Action
		n    SQL statement n
	Reward:
		+10 for capturing the flag, -1 in all the other cases.
	Starting State:
		Webserver initialized with a random query. No action tested.
	Episode Termination:
		Capture the flag.
	"""

	metadata = {'render.modes': ['human', 'ansi']}

	def __init__(self):
		# Action space
		self.action_space = spaces.Discrete(51)

		# Observation space
		self.observation_space = spaces.MultiDiscrete(np.ones(51)*3)

		# State
		self.state = np.ones(51)

		# Random integers to setup the server
		r = np.random.randint(3)
		f = np.random.randint(5)
		self.flag_cols = f

		# The random setup contains the correct escape sequences and the correct SQL injection
		self.setup = [0+r*17, 1+r*17,(12+f)+r*17]

		# Get the set of actions that are syntactically correct
		self.syntaxmin = 0+r*17
		self.syntaxmax = 17+r*17

		self.done = False
		self.verbose = False
		if(self.verbose): print('Game setup with a random query')

		self.seed()
		self.viewer = None
		#self.steps_beyond_done = None

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]


	def step(self, action):
		assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

		"""
		0neg
		1neut
		2pos
		"""
		# Process action
		if (action==self.setup[0]):
			if(self.verbose): print('Correct escape 2')
			self.state[action] = 2
			return self.state,-1,self.done,{'msg':'Server response is 2'}
		elif (action==self.setup[1]):
			if(self.verbose): print('Correct escape. But still nothing I return 0')
			self.state[action] = 0
			return self.state,-1,self.done,{'msg':'Server response is 0'}
		elif (action==self.setup[2]):
			if(self.verbose): print('Flag captured. I return 2')
			self.done = True
			self.state[action] = 2
			return self.state,10,self.done,{'msg':'FLAG Server response is 2'}
		elif (action >= self.syntaxmin and action < self.syntaxmax):
			if(action == self.flag_cols*2 + self.setup[1] + 1 or action == self.flag_cols*2 + self.setup[1] + 2):
				if(self.verbose): print('Query with correct number of rows')
				self.state[action] = 2
				return self.state,-1,self.done,{'msg':'Server response is 2'}

			if(self.verbose):
				print('Query has the correct escape, but contains the wrong number of rows. I return 0')
			self.state[action] = 0
			return self.state,-1,self.done,{'msg':'Server response is 0 wrong number of rows'}
		else:
			if(self.verbose): print('Query is syntactically wrong. I return 0')
			self.state[action] = 0
			return self.state,-1,self.done,{'msg':'Server response is 0'}

	def reset(self):
		self.done = False
		self.state = np.ones(51)

		# Reinitializing the random query        
		r = np.random.randint(3)
		f = np.random.randint(5)
		self.flag_cols = f
		self.setup = [0+r*17, 1+r*17,(12+f)+r*17]
		self.syntaxmin = 0+r*17
		self.syntaxmax = 17+r*17
        
		if(self.verbose): print('Game reset (with a new random query!)')
		return self.state#,0,self.done,{'msg':'Game reset'}


	def render(self, mode='human'):
		return None

	def close(self):
		return
