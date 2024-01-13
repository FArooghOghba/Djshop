from typing import (
    Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, TypeVar,
)

from . import utils
from .base import Factory


T = TypeVar('T')

logger: Any


class BaseDeclaration(utils.OrderedBase):
    FACTORY_BUILDER_PHASE: bool

    CAPTURE_OVERRIDES: bool = ...
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool = ...

    def __init__(self, **defaults: Any) -> None: ...

    def unroll_context(self, instance: T, step: int, context: Dict[str, Any]) -> None: ...

    def evaluate_pre(self, instance: T, step: int, overrides: Dict[str, Any]) -> None: ...

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> None: ...


class OrderedDeclaration(BaseDeclaration): ...


class LazyFunction(BaseDeclaration):
    function: Callable[..., Any]

    def __init__(self, function: Callable[..., Any]) -> None: ...

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> Any: ...


class LazyAttribute(BaseDeclaration):
    function: Callable[[], Any]

    def __init__(self, function: Callable[[Any], Any]) -> None: ...

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> Any: ...


class Transformer(BaseDeclaration):
    CAPTURE_OVERRIDES: bool = ...
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool = ...

    class Force:
        forced_value: Any

        def __init__(self, forced_value: Any) -> None: ...

    default: Any
    transform: Callable[[Any], Any]

    def __init__(self, default: Any, *, transform: Callable[[Any], Any]) -> None: ...

    def evaluate_pre(self, instance: T, step: int, overrides: Dict[str, Any]) -> None: ...


class _UNSPECIFIED: ...


def deepgetattr(obj: Any, name: str, default: Any = ...) -> Any: ...


class SelfAttribute(BaseDeclaration):
    depth: int
    attribute_name: str
    default: Any

    def __init__(self, attribute_name: str, default: Any = ...) -> None: ...

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> Any: ...


class Iterator(BaseDeclaration):
    getter: Optional[Callable[[Any], Any]]
    iterator: Iterable[Any]
    iterator_builder: Optional[Callable[[], Iterable[Any]]]

    def __init__(
            self,
            iterator: Iterable[Any],
            cycle: bool = ...,
            getter: Optional[Callable[[Any], Any]] = ...
    ) -> None: ...

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> Any: ...

    def reset(self) -> None: ...


class Sequence(BaseDeclaration):
    function: Callable[[int], Any]

    def __init__(self, function: Callable[[int], Any]) -> None: ...

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> Any: ...


class LazyAttributeSequence(Sequence):

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> Any: ...


class ContainerAttribute(BaseDeclaration):
    function: Callable[..., List[Any]]
    strict: bool

    def __init__(self, function: Callable[..., List[Any]], strict: bool = ...) -> None: ...

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> None: ...


class ParameteredAttribute(BaseDeclaration):

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> Any: ...

    def generate(self, step: int, params: Dict[str, Any]) -> None: ...


class _FactoryWrapper:
    factory: Type[Factory]
    module: str

    def __init__(self, factory_or_path: str) -> None: ...

    def get(self) -> Type[Factory]: ...


class SubFactory(BaseDeclaration):
    FORCE_SEQUENCE: bool = ...
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool = ...

    factory_wrapper: _FactoryWrapper

    def __init__(self, factory: Type[Factory], **kwargs: Any) -> None: ...

    def get_factory(self) -> Type[Factory]: ...

    def evaluate(self, instance: T, step: int, extra: Dict[str, Any]) -> Any: ...


class Skip:

    def __bool__(self) -> bool: ...


SKIP: Skip


class Maybe(BaseDeclaration):
    decider: Callable[..., bool]
    yes: BaseDeclaration
    no: BaseDeclaration

    FACTORY_BUILDER_PHASE: bool = ...

    def __init__(
            self,
            decider: Callable[..., bool],
            yes_declaration: Optional[BaseDeclaration] = ...,
            no_declaration: Optional[BaseDeclaration] = ...
    ) -> None: ...

    def evaluate_post(self, instance: T, step: int, overrides: Dict[str, Any]) -> None: ...

    def evaluate_pre(self, instance: T, step: int, overrides: Dict[str, Any]) -> None: ...


class Parameter(utils.OrderedBase):

    def as_declarations(self, field_name: str, declarations: List[BaseDeclaration]) -> None: ...

    def get_revdeps(self, parameters: Dict[str, 'Parameter']) -> List[str]: ...


class SimpleParameter(Parameter):
    value: Any

    def __init__(self, value: Any) -> None: ...

    def as_declarations(self, field_name: str, declarations: List[BaseDeclaration]) -> None: ...

    @classmethod
    def wrap(cls, value: Any) -> 'SimpleParameter': ...


class Trait(Parameter):
    overrides: Dict[str, Any]

    def __init__(self, **overrides: Any) -> None: ...

    def as_declarations(self, field_name: str, declarations: List[BaseDeclaration]) -> None: ...

    def get_revdeps(self, parameters: Dict[str, 'Parameter']) -> List[str]: ...


class PostGenerationContext(Tuple[bool, Any, Dict[str, Any]]): ...


class PostGenerationDeclaration(BaseDeclaration):
    FACTORY_BUILDER_PHASE: bool = ...

    def evaluate_post(self, instance: T, step: int, overrides: Dict[str, Any]) -> None: ...

    def call(self, instance: T, step: int, context: PostGenerationContext) -> None: ...


class PostGeneration(PostGenerationDeclaration):
    function: Callable[[T, PostGenerationContext], None]

    def __init__(self, function: Callable[[T, PostGenerationContext], None]) -> None: ...

    def call(self, instance: T, step: int, context: PostGenerationContext) -> None: ...


class RelatedFactory(PostGenerationDeclaration):
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool = ...

    name: Optional[str]
    defaults: Dict[str, Any]
    factory_wrapper: _FactoryWrapper

    def __init__(
            self,
            factory: Type[Factory],
            factory_related_name: str = ...,
            **defaults: Any
    ) -> None: ...

    def get_factory(self) -> Type[Factory]: ...

    def call(self, instance: T, step: int, context: PostGenerationContext) -> None: ...


class RelatedFactoryList(RelatedFactory):
    size: int

    def __init__(
            self,
            factory: Type[Factory],
            factory_related_name: str = ...,
            size: int = ...,
            **defaults: Any
    ) -> None: ...

    def call(self, instance: T, step: int, context: PostGenerationContext) -> None: ...


class NotProvided: ...


class PostGenerationMethodCall(PostGenerationDeclaration):
    method_name: str
    method_arg: Any
    method_kwargs: Dict[str, Any]

    def __init__(
            self,
            method_name: str,
            *args: Any,
            **kwargs: Any
    ) -> None: ...

    def call(self, instance: T, step: int, context: PostGenerationContext) -> None: ...
