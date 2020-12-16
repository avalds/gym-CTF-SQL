"""
Copy of a copy: This was copied from https://raw.github.uio.no/fabiomz/gym-qiscoin/master/qiscoin/envs/qiscoin_env.py?token=AAAAD6HUBAQR2F23OOP454274OQHC
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

from qiskit import QuantumCircuit, Aer, execute



class CTFSQLEnv0(gym.Env):
	"""
	WIPWIPWIP
	Description:
		A quantum circuit with 1 qubit (and 1 classical bit) is given. A random gate is added. Guess the measurement.
	Observation:
		Type: Discrete(6)
		Num    Observation
		0   h
		1   x
		2   reset
		3   t
		4   tdg
		5   iden
	Actions:
		Type: Discrete(2)
		Num    Action
		0    Guess 0
		1    Guess 1
	Reward:
		0 for guessing wrong, +1 for guessing right.
	Starting State:
		Circuit with 1 quantum and 1 classical bit and 1 random gate.
	Episode Termination:
		One guess
	"""

	metadata = {'render.modes': ['human', 'ansi']}

	def __init__(self):
		# State
		self.simulator = Aer.get_backend('qasm_simulator')
		self.circuit = QuantumCircuit(1,1)
		self.n_components = 1
		self.components = [self.circuit.h, self.circuit.x, self.circuit.reset, self.circuit.t, self.circuit.tdg, self.circuit.iden]

		# Observation space
		self.observation_space = spaces.Discrete(6)

		# Action space
		self.action_space = spaces.Discrete(2)

		self.seed()
		self.viewer = None
		#self.steps_beyond_done = None

		self.listcomponents = []
		for i in range(self.n_components):
			index = np.random.choice(6)
			self.components[index](0)
			self.listcomponents.append(index)
		self.circuit.measure(0,0)
		self.state = self.listcomponents[0]

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]

	def step(self, action):
		assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

		results = execute(self.circuit, backend = self.simulator, shots = 1).result()
		counts = results.get_counts()
		if(counts.get(str(action*1), 0)):
			reward = 1.
		else:
			reward = -1.

		done = True

		return np.array(self.state), reward, done, {}

	def reset(self):
		self.circuit = QuantumCircuit(1,1)
		self.components = [self.circuit.h, self.circuit.x, self.circuit.reset, self.circuit.t, self.circuit.tdg, self.circuit.iden]
		self.listcomponents = []
		for i in range(self.n_components):
			index = np.random.choice(6)
			self.components[index](0)
			self.listcomponents.append(index)
		self.circuit.measure(0,0)
		self.state = self.listcomponents[0]
		return np.array(self.state)

	def render(self, mode='human'):
		return self.circuit.draw(output='mpl')

	def close(self):
		return
