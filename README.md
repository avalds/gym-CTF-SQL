# gym-CTF-SQL

Implementation of CTF-SQL environment for OpenAI gym used at https://github.com/FMZennaro/CTF-SQL.

### Requirements
The following code requires *numpy* and [OpenAI gym](https://github.com/openai/gym).

### Installation
Clone this git and run `pip install -e gym-CTF-SQL` to make this environment available to *OpenAI gym*.

### Content
The project *gym-CTF-SQL* contains the implementation of a simple server running a webpage with a SQL injection vulnerability.

- *CTFSQLEnv0*: this class instantiate an environment running a server with a SQL injection vulnerability. The action space, the observation space, and the random initialization of the vulnerability are explained in [1].


### Use
First, import *numpy*, *OpenAI gym* and *gym-CTF-SQL*:

```python
import numpy as np
import gym
import ctfsql
```
Then, you can simply instantiate a new environment and start using it:
```python
env = gym.make('ctfsql-v0')
```

### References
\[1\] Erdodi, L., Sommervoll, A.A. and Zennaro, F.M., 2020. Simulating SQL Injection Vulnerability Exploitation Using Q-Learning Reinforcement Learning Agents. arXiv preprint.

