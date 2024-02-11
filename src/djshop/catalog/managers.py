from treebeard.mp_tree import MP_Node, MP_NodeQuerySet


class CategoryQuerySet(MP_NodeQuerySet[MP_Node]):

    """
    Custom queryset for the Category model.

    This queryset provides additional methods for querying Category objects.

    Methods:
        public(): Returns a queryset containing only public categories.
    """

    def public(self) -> 'CategoryQuerySet':

        """
        Filter the queryset to include only public categories.

        :returns: CategoryQuerySet: A queryset containing only public categories.
        """

        return self.filter(is_public=True)
