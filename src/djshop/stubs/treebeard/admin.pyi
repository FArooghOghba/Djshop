from typing import Any, Optional, Type

from django.contrib import admin
from django.http import HttpRequest
from treebeard.al_tree import AL_Node as AL_Node
from treebeard.models import Node


class TreeAdmin(admin.ModelAdmin[Node]):

    change_list_template: str

    def get_queryset(self, request: HttpRequest) -> Any: ...

    def changelist_view(
        self, request: HttpRequest, extra_context: Optional[dict[str, Any]] = None
    ) -> Any: ...

    def get_urls(self) -> list[Any]: ...

    def get_node(self, node_id: int) -> AL_Node: ...

    def try_to_move_node(
            self, as_child: bool, node: AL_Node, pos: str,
            request: HttpRequest, target: AL_Node
    ) -> None: ...

    def move_node(self, request: HttpRequest) -> None: ...


def admin_factory(
    form_class: Type[Any]
) -> Type[TreeAdmin]: ...
