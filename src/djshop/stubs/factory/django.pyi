from typing import Any, Optional, Type

from django.db.models import Model

from . import base as base, declarations as declarations


logger: Any
DEFAULT_DB_ALIAS: str


def get_model(app: str, model: str) -> Type[Model]: ...

class DjangoOptions(base.FactoryOptions):
    model: Type[Model]

    def get_model_class(self) -> Type[Model]: ...

class DjangoModelFactory(base.Factory):
    class Meta:
        abstract: bool

class Password(declarations.Transformer):
    def __init__(
            self, password: str, transform: Optional[Any] = ..., **kwargs: Any
    ) -> None: ...

class FileField(declarations.BaseDeclaration):
    DEFAULT_FILENAME: str

    def evaluate(
            self, instance: Any, step: int, extra: Optional[Any]
    ) -> None: ...

class ImageField(FileField):
    DEFAULT_FILENAME: str

class mute_signals:
    signals: Any
    paused: bool

    def __init__(self, *signals: Any) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[Any]
    ) -> None: ...

    def copy(self) -> 'mute_signals': ...

    def __call__(self, callable_obj: Any) -> Any: ...

    def wrap_method(self, method: Any) -> Any: ...
