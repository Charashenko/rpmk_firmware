class Event:
    ON_DETECT = 0
    ON_SCAN_ROUND_END = 1
    ON_PRESS = 2
    ON_RELEASE = 3

    def __init__(self, event_type: int, event_data: object = None):
        self.type = event_type
        self.data = event_data
