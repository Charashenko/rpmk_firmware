from .event import Event
from ..utils.log import Logger

log = Logger(__name__)
subscribers = {}
executor = None


def post_event(event: Event):
    for key in subscribers.keys():
        if key is event.type:
            for subscriber in subscribers[key]:
                # log.d(
                #     f'Posting event "{event.type}" to subscribed function "{subscriber}" with data "{event.data}"'
                # )
                subscriber(executor, event)
            return

    log.w(f'No subcribers for event type: "{event.type}"')


def subscribe(event: Event):
    def wrapper_func(func):
        def wrapper_subscribe():
            if event.type in subscribers.keys():
                subscribers[event.type].append(func)
            else:
                subscribers[event.type] = [func]
            log.d(f'Func "{func}" subscribed to event "{event.type}"')
            return func

        return wrapper_subscribe()

    return wrapper_func


def unsubscribe(event: Event):
    def wrapper_func(func):
        def wrapper_unsubscribe():
            if event in subscribers.keys():
                if func in subscribers[event]:
                    subscribers[event].remove(func)
                    log.d(f'Func "{func}" unsubscribed from event "{event}"')
            return func

        return wrapper_unsubscribe()

    return wrapper_func


def register_executor(exe):
    executor = exe
