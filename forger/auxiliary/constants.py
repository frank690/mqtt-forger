# used by forger.engine.manager
DEFAULT_PIPELINE_SETTINGS = {
    "channel_scale": None,
    "channel_frequency": 0.1,
    "channel_type": "sin",
    "pipeline_name": "Pipe",
    "dead_frequency": 1.0,
    "dead_period": 0.0,
    "replay_data": None,
}

# used by forger.engine.painter
MAX_DELAY = 1 / (24 * 60 * 60)  # 1 second
MEMORY = 5 / (24 * 60 * 60)  # 5 seconds
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
DISPLAY_DATE_FORMAT = "%M:%S"
