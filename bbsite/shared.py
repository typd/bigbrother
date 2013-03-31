import cfg

FIRST_TIME = None
TOTAL_DAYS = 0
DATA = []
WEEKDAY_STACK_INTERVAL = 24 / cfg.WEEKDAY_STACKS
WEEKDAY_STACK_NAMES = ["{}:00-{}:59".format(
        idx * WEEKDAY_STACK_INTERVAL,
        (idx + 1) * WEEKDAY_STACK_INTERVAL - 1)
        for idx in range(0, cfg.WEEKDAY_STACKS)]
