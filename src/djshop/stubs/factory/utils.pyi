from typing import Any, Callable, Iterable, List, Optional


def import_object(module_name: str, attribute_name: str) -> Any: ...

class log_pprint:
    args: Any
    kwargs: Any

    def __init__(self, args: Any = ..., kwargs: Any | None = None) -> None: ...

class ResetableIterator:
    iterator: Any
    past_elements: Any
    next_elements: Any

    def __init__(self, iterator: Any, **kwargs: Any) -> None: ...
    def __iter__(self) -> Any: ...
    def reset(self) -> None: ...

class OrderedBase:
    CREATION_COUNTER_FIELD: str

    def __init__(self, **kwargs: Any) -> None: ...
    def touch_creation_counter(self) -> None: ...

def sort_ordered_objects(
    items: Iterable[Any],
    getter: Optional[Callable[[Any], Any]] = ...
) -> List[Any]: ...
