from typing import Any, Dict, List, Type, TypeVar

from django.db import models
from treebeard.models import Node as Node  # type: ignore
from treebeard.numconv import NumConv as NumConv  # type: ignore


T = TypeVar('T')


def sql_concat(*args: str, **kwargs: Any) -> str: ...

def sql_length(field: str, vendor: None = ...) -> str: ...

def sql_substr(field: str, pos: int, length: None = ..., **kwargs: Any) -> str: ...

def get_result_class(cls: Type[MP_Node]) ->  Type[MP_Node]: ...


class MP_NodeQuerySet(models.query.QuerySet[MP_Node]):

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]: ...


class MP_NodeManager(models.Manager[MP_Node]):

    def get_queryset(self) -> MP_NodeQuerySet: ...


class MP_AddHandler:

    stmts: List[str]

    def __init__(self) -> None: ...


class MP_ComplexAddMoveHandler(MP_AddHandler):

    def run_sql_stmts(self) -> None: ...

    def get_sql_update_numchild(self, path: str, incdec: str = 'inc') -> str: ...

    def reorder_nodes_before_add_or_move(
            self,
            pos: int,
            newpos: int,
            newdepth: int,
            target: MP_Node,
            siblings: List[MP_Node],
            oldpath: None = ...,
            movebranch: bool = ...
    ) -> None: ...

    def get_sql_newpath_in_branches(self, oldpath: str, newpath: str) -> str: ...


class MP_AddRootHandler(MP_AddHandler):

    cls: Type[MP_Node]
    kwargs: Dict[str, Any]

    def __init__(self, cls:  Type[MP_Node], **kwargs: Any) -> None: ...

    def process(self) -> MP_Node: ...


class MP_AddChildHandler(MP_AddHandler):

    node: MP_Node
    node_cls:  Type[MP_Node]
    kwargs: Dict[str, Any]

    def __init__(self, node: MP_Node, node_cls:  Type[MP_Node], **kwargs: Any) -> None: ...

    def process(self) -> MP_Node: ...


class MP_AddSiblingHandler(MP_ComplexAddMoveHandler):

    node: MP_Node
    node_cls:  Type[MP_Node]
    pos: int
    kwargs: Dict[str, Any]

    def __init__(
            self, node: MP_Node, node_cls: Type[MP_Node], pos: int, **kwargs: Any
    ) -> None: ...

    def process(self) -> MP_Node: ...


class MP_MoveHandler(MP_ComplexAddMoveHandler):

    node: MP_Node
    node_cls: Type[MP_Node]
    target: MP_Node
    pos: None | int

    def __init__(self, node: MP_Node, target: MP_Node, pos: None | int = ...) -> None: ...

    def process(self) -> None: ...

    def sanity_updates_after_move(self, oldpath: str, newpath: str) -> None: ...

    def update_move_to_child_vars(self) -> None: ...

    def get_mysql_update_depth_in_branch(self, path: str) -> str: ...

class MP_Node(Node):  # type: ignore

    steplen: int
    alphabet: str
    node_order_by: List[str]
    path: str
    depth: int
    numchild: int
    gap: int
    objects: Any
    numconv_obj_: Any

    @classmethod
    def _int2str(cls, num: int) -> str: ...

    @classmethod
    def _str2int(cls, num: str) -> int: ...

    @classmethod
    def numconv_obj(cls) -> NumConv: ...

    @classmethod
    def add_root(cls: Type[T], **kwargs: Any) -> T: ...

    @classmethod
    def dump_bulk(cls, parent: MP_Node = ..., keep_ids: bool = True) -> List[Dict[str, str]]: ...
    # Example return type: List of dictionaries with string keys and values.

    # Define other methods with type hints based on their usage and return types

    class Meta:
        abstract: bool
