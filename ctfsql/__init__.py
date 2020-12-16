from gym.envs.registration import register

register(
    id='ctfsql-v0',
    entry_point='ctfsql.envs:CTFSQLEnv0',
)
