from typing import Callable, Dict, List, Type

class EventDispatcher:
    """
    In-memory synchronous event dispatcher.
    Runs registered handlers immediately in the same thread and transaction context.
    """
    def __init__(self):
        self._listeners: Dict[Type, List[Callable]] = {}

    def subscribe(self, event_type: Type, listener: Callable) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def dispatch(self, event: object) -> None:
        event_type = type(event)
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(event)
