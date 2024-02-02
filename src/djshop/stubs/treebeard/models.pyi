from typing import Any, Optional, Type, TypeVar

from django.db import models


T = TypeVar('T')


class Node(models.Model):

    @classmethod
    def add_root(cls: Type[T], **kwargs: Any) -> T: ...

    @classmethod
    def get_foreign_keys(cls) -> list[models.Field[Any, Any]]: ...

    @classmethod
    def load_bulk(
        cls,
        bulk_data: list[dict[str, Any]],
        parent: Optional['Node'] = None,
        keep_ids: bool = True
    ) -> None: ...

    @classmethod
    def dump_bulk(
        cls,
        parent: Optional['Node'] = None,
        keep_ids: bool = True
    ) -> list['Node']: ...

    @classmethod
    def get_root_nodes(cls) -> models.QuerySet['Node']: ...

    @classmethod
    def get_first_root_node(cls) -> 'Node': ...

    @classmethod
    def get_last_root_node(cls: Type[T]) -> 'T': ...

    @classmethod
    def find_problems(cls) -> list[str]: ...

    @classmethod
    def fix_tree(cls) -> None: ...

    @classmethod
    def get_tree(
        cls,
        parent: Optional['Node'] = None
    ) -> models.QuerySet['Node']: ...

    @classmethod
    def get_descendants_group_count(
        cls,
        parent: Optional['Node'] = None
    ) -> dict[int, int]: ...

    def get_depth(self) -> int: ...

    def get_siblings(self) -> models.QuerySet['Node']: ...

    def get_children(self) -> models.QuerySet['Node']: ...

    def get_children_count(self) -> int: ...

    def get_descendants(self) -> models.QuerySet['Node']: ...

    def get_descendant_count(self) -> int: ...

    def get_first_child(self) -> Optional['Node']: ...

    def get_last_child(self) -> Optional['T']: ...

    def get_first_sibling(self) -> Optional['Node']: ...

    def get_last_sibling(self) -> Optional['Node']: ...

    def get_prev_sibling(self) -> Optional['Node']: ...

    def get_next_sibling(self) -> Optional['Node']: ...

    def is_sibling_of(self, node: 'Node') -> bool: ...

    def is_child_of(self, node: 'Node') -> bool: ...

    def is_descendant_of(self, node: 'Node') -> bool: ...

    def add_child(self, **kwargs: Any) -> Optional['T']: ...

    def add_sibling(
        self,
        pos: Optional[str] = None,
        **kwargs: Any
    ) -> 'Node': ...
