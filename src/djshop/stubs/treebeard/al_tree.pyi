from typing import Any, Optional, Type, TypeVar

from django.db import models
from treebeard.models import Node


T = TypeVar('T')


def get_result_class(cls: Type[AL_Node]) -> Type[AL_Node]: ...


class AL_NodeManager(models.Manager[Node]):

    def get_queryset(self) -> models.QuerySet[AL_Node]: ...


class AL_Node(Node):
    objects: AL_NodeManager

    node_order_by: list[str]

    @classmethod
    def add_root(cls, **kwargs: Any) -> AL_Node: ...

    @classmethod
    def get_root_nodes(cls) -> models.QuerySet[AL_Node]: ...

    def get_depth(self, update: bool = False) -> int: ...

    def get_children(self) -> models.QuerySet[AL_Node]: ...

    def get_parent(self, update: bool = False) -> Optional[AL_Node]: ...

    def get_ancestors(self) -> models.QuerySet[AL_Node]: ...

    def get_root(self) -> AL_Node: ...

    def is_descendant_of(self, node: Node) -> bool: ...

    @classmethod
    def dump_bulk(
            cls,
            parent: Optional[Node] = None,
            keep_ids: bool = True
    ) -> list[Node]: ...

    def add_child(self, **kwargs: Any) -> Optional['T']: ...

    @classmethod
    def get_tree(
            cls,
            parent: Optional[Node] = None
    ) -> models.QuerySet[Node]: ...

    def get_descendants(self) -> models.QuerySet[AL_Node]: ...

    def get_descendant_count(self) -> int: ...

    def get_siblings(self) -> models.QuerySet[AL_Node]: ...

    def add_sibling(self, pos: Optional[str] = None, **kwargs: Any) -> AL_Node: ...

    parent: Optional[AL_Node]

    sib_order: int

    def move(self, target: AL_Node, pos: Optional[str] = None) -> None: ...

    class Meta:
        abstract = True
