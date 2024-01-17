from typing import Any, Callable, Optional, Type, Union

from django import forms
from treebeard.al_tree import AL_Node
from treebeard.mp_tree import MP_Node
from treebeard.ns_tree import NS_Node  # type: ignore


class MoveNodeForm(forms.ModelForm[Any]):

    is_sorted: bool

    def __init__(
            self,
            data: Optional[dict[str, Any]] = None,
            files: Optional[dict[str, Any]] = None,
            auto_id: str = ...,
            prefix: Optional[str] = None,
            initial: Optional[dict[str, Any]] = None,
            error_class: Type[Exception] = ...,
            label_suffix: str = ...,
            empty_permitted: bool = ...,
            instance: Optional[Union[AL_Node, MP_Node, NS_Node]] = None,
            **kwargs: Any
    ) -> None:
        ...

    instance: Optional[Union[AL_Node, MP_Node, NS_Node]]

    def save(self, commit: bool = ...) -> Any:
        ...

    @staticmethod
    def is_loop_safe(
            for_node: Union[AL_Node, MP_Node, NS_Node],
            possible_parent: Union[AL_Node, MP_Node, NS_Node]
    ) -> bool:
        ...

    @staticmethod
    def mk_indent(level: int) -> str:
        ...

    @classmethod
    def add_subtree(
            cls,
            for_node: Union[AL_Node, MP_Node, NS_Node],
            node: Union[AL_Node, MP_Node, NS_Node],
            options: dict[str, Any]
    ) -> None:
        ...

    @classmethod
    def mk_dropdown_tree(
            cls,
            model: Type[Union[AL_Node, MP_Node, NS_Node]],
            for_node: Optional[Union[AL_Node, MP_Node, NS_Node]] = None
    ) -> dict[str, list[Any]]:
        ...


def movenodeform_factory(
        model: Type[Union[AL_Node, MP_Node, NS_Node]],
        form: Type[MoveNodeForm] = MoveNodeForm,
        fields: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
        formfield_callback: Optional[Callable[..., Any]] = None,
        widgets: Optional[dict[str, Any]] = None
) -> Type[MoveNodeForm]:
    ...
