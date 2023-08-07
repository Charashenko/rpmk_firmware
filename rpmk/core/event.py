from ..utils.log import Logger

log = Logger(name)
subscribers = {}

ON_DETECT = (0, "ON_DETECT")
ON_SYS_PRESS = (1, "ON_SYS_PRESS")
ON_SYS_LAYER = (2, "ON_SYS_LAYER")


def post_event(event_type: str, event_data: object):
    if event_type in subscribers.keys():
        for event_listener in subscribers.get(event_type):
            log.d(
                msg=f'Sending event of type "{event_type}" to "{event_listener}" with data "{event_data}"',
            )
            event_listener.handler(event_type, event_data)


def subscribe(event_type: str, event_listener: object):
    if event_type not in subscribers.keys():
        subscribers[event_type] = [event_listener]
    else:
        subscribers.get(event_type).append(event_listener)
    log.d(
        msg=f'"{event_listener}" subscribed to "{event_type}"',
    )


def unsubscribe(event_type: str, event_listener: object):
    if event_type not in subscribers.keys():
        return
    try:
        subscribers[event_type].remove(event_listener)
        log.d(
            msg=f'"{event_listener}" unsubscribed from "{event_type}"',
        )
    except ValueError:
        log.w(
            msg=f'"{event_listener}" doesn\'t contain "{event_type}"',
        )
