from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

from . import declarations


T = TypeVar('T')

logger: Any


def get_factory_bases(bases: tuple[Type[Factory]]) -> tuple[Type[Factory], ...]: ...

def resolve_attribute(
    name: str, bases: tuple[Type[Factory]], default: Optional[Any] = ...
) -> Any: ...

class FactoryMetaClass(type):
    def __call__(cls: T, **kwargs: Any) -> T: ...
    def __new__(
            mcs, class_name: str, bases: tuple[Type[Factory]], attrs: Dict[str, Any]
    ) -> Type[T]: ...

class BaseMeta:
    abstract: bool
    strategy: Optional[str]

class OptionDefault:
    name: str
    value: Any
    inherit: bool
    checker: Optional[Callable[[Any], bool]]

    def __init__(
            self,
            name: str,
            value: Any,
            inherit: bool = ...,
            checker: Optional[Callable[[Any], bool]] = ...
    ) -> None: ...

    def apply(self, meta: BaseMeta, base_meta: Optional[BaseMeta]) -> None: ...

class FactoryOptions:
    factory: Type[Factory]
    base_factory: Optional[Type[Factory]]
    base_declarations: Dict[str, declarations.BaseDeclaration]
    parameters: Dict[str, declarations.Parameter]
    parameters_dependencies: Dict[str, str]
    pre_declarations: List[declarations.BaseDeclaration]
    post_declarations: List[declarations.BaseDeclaration]
    counter_reference: Optional[str]

    def __init__(self) -> None: ...

    @property
    def declarations(self) -> Dict[str, declarations.BaseDeclaration]: ...

    model: Type[Any]
    abstract: bool

    def contribute_to_class(
            self,
            factory: Type[Factory],
            meta: Optional[BaseMeta] = ...,
            base_meta: Optional[BaseMeta] = ...,
            base_factory: Optional[Type[Factory]] = ...,
            params: Optional[Dict[str, Any]] = ...
    ) -> None: ...

    def next_sequence(self) -> None: ...

    def reset_sequence(self, value: Optional[int] = ..., force: bool = ...) -> None: ...

    def prepare_arguments(self, attributes: Dict[str, Any]) -> Dict[str, Any]: ...

    def instantiate(self, step: int, args: List[Any], kwargs: Dict[str, Any]) -> Any: ...

    def use_postgeneration_results(self, step: int, instance: T, results: Dict[str, Any]) -> None: ...

    def get_model_class(self) -> Type[Any]: ...


class _Counter:
    seq: int

    def __init__(self, seq: int) -> None: ...

    def next(self) -> int: ...

    def reset(self, next_value: int = ...) -> None: ...


class BaseFactory:

    UnknownStrategy: Any
    UnsupportedStrategy: Any

    def __new__(cls, *args: Any, **kwargs: Any) -> Factory: ...

    @classmethod
    def reset_sequence(cls, value: Optional[int] = ..., force: bool = ...) -> None: ...

    @classmethod
    def build(cls: T, **kwargs: Any) -> T: ...

    @classmethod
    def build_batch(cls: T, size: int, **kwargs: Any) -> List[T]: ...

    @classmethod
    def create(cls: T, **kwargs: Any) -> T: ...

    @classmethod
    def create_batch(cls: T, size: int, **kwargs: Any) -> List[T]: ...

    @classmethod
    def stub(cls, **kwargs: Any) -> StubObject: ...

    @classmethod
    def stub_batch(cls, size: int, **kwargs: Any) -> List[StubObject]: ...

    @classmethod
    def generate(cls: T, strategy: Optional[str], **kwargs: Any) -> T: ...

    @classmethod
    def generate_batch(cls, strategy: Optional[str], size: int, **kwargs: Any) -> List[T]: ...

    @classmethod
    def simple_generate(cls, create: Callable[[], T], **kwargs: Any) -> T: ...

    @classmethod
    def simple_generate_batch(cls, create: Callable[[], T], size: int, **kwargs: Any) -> List[T]: ...


class Factory(BaseFactory, metaclass=FactoryMetaClass):
    class Meta(BaseMeta): ...

class StubObject:
    def __init__(self, **kwargs: Any) -> None: ...

class StubFactory(Factory):
    class Meta:
        strategy: Optional[str]
        model = StubObject

    @classmethod
    def build(cls: T, **kwargs: Any) -> T: ...

    @classmethod
    def create(cls: T, **kwargs: Any) -> T: ...

class BaseDictFactory(Factory):
    class Meta:
        abstract: bool

class DictFactory(BaseDictFactory):
    class Meta:
        model = Dict[Any, Any]

class BaseListFactory(Factory):
    class Meta:
        abstract: bool

class ListFactory(BaseListFactory):
    class Meta:
        model = List[Any]

def use_strategy(new_strategy: Optional[str]) -> None: ...
