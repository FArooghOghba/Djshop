from typing import Any, Dict, List, Optional, Type, TypeVar

from django.db import models
from treebeard.models import Node as Node
from treebeard.numconv import NumConv as NumConv  # type: ignore


T = TypeVar('T')
ModelType = TypeVar('ModelType', bound=models.Model)


def sql_concat(*args: str, **kwargs: Any) -> str: ...

def sql_length(field: str, vendor: None = ...) -> str: ...

def sql_substr(field: str, pos: int, length: None = ..., **kwargs: Any) -> str: ...

def get_result_class(cls: Type[MP_Node]) ->  Type[MP_Node]: ...


class MP_NodeQuerySet(models.query.QuerySet[ModelType]):

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]: ...


class MP_NodeManager(models.Manager[MP_Node]):

    def get_queryset(self) -> MP_NodeQuerySet[ModelType]: ...


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

class MP_Node(Node):

    steplen: int
    alphabet: str
    node_order_by: List[str]
    path: str
    depth: int
    numchild: int
    gap: int
    objects: MP_NodeManager
    numconv_obj_: NumConv

    @classmethod
    def _int2str(cls, num: int) -> str: ...

    @classmethod
    def _str2int(cls, num: str) -> int: ...

    @classmethod
    def numconv_obj(cls) -> NumConv: ...

    @classmethod
    def add_root(cls: Type[T], **kwargs: Any) -> T: ...

    @classmethod
    def dump_bulk(cls, parent: Optional[Node] = None, keep_ids: bool = True) -> List[Node]: ...
    # Example return type: List of dictionaries with string keys and values.

    @classmethod
    def find_problems(cls) -> List[str]: ...

    @classmethod
    def fix_tree(cls, destructive: bool = ..., fix_paths: bool = ...) -> None: ...

    @classmethod
    def get_tree(cls, parent: Optional['Node'] = None) -> models.QuerySet['Node']: ...

    @classmethod
    def get_root_nodes(cls: Type[ModelType]) -> MP_NodeQuerySet[ModelType]: ...

    @classmethod
    def get_descendants_group_count(cls, parent: Optional['Node'] = None) -> dict[int, int]: ...

    def get_depth(self) -> int: ...

    def get_siblings(self) -> MP_NodeQuerySet[ModelType]: ...

    def get_children(self) -> MP_NodeQuerySet[ModelType]: ...

    def get_next_sibling(self) -> MP_Node | None: ...

    def get_descendants(self) -> MP_NodeQuerySet[ModelType]: ...

    def get_prev_sibling(self) -> MP_Node | None: ...

    def get_children_count(self) -> int: ...

    def is_sibling_of(self, node: Node) -> bool: ...

    def is_child_of(self, node: Node) -> bool: ...

    def is_descendant_of(self, node: Node) -> bool: ...

    def add_child(self, **kwargs: Any) -> Optional['T']: ...

    def add_sibling(self, pos: Optional[str] = None, **kwargs: Any) -> MP_Node: ...

    def get_root(self) -> MP_Node: ...

    def is_root(self) -> bool: ...

    def is_leaf(self) -> bool: ...

    def get_ancestors(self) -> MP_NodeQuerySet[ModelType]: ...

    def get_parent(self, update: bool = ...) -> MP_Node | None: ...

    def move(self, target: MP_Node, pos: int | None = ...) -> None: ...

    class Meta:
        abstract: bool
