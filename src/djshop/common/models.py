from typing import TYPE_CHECKING, Any, Optional, TypedDict, Union

from django.db import models
from django.db.models import F, Q
from django.db.models.expressions import Combinable

from src.config.django.base import AUTH_USER_MODEL


if TYPE_CHECKING:
    from src.djshop.users.models import BaseUser


BaseUserOrNone = Union['BaseUser', Combinable, None]


class RelatedNames(TypedDict):
    """
    Typed dictionary representing related names for created and updated fields.

    Attributes:
        created (str): The related name for the created_by field.
        updated (str): The related name for the updated_by field.
    """

    created: str
    updated: str


class BaseModel(models.Model):

    """
    Base model that includes common fields used across multiple models.

    Fields:
    - created_at: DateTimeField representing the creation timestamp.
    - created_by: ForeignKey to BaseUser or None, representing the user
                who created the instance.
    - updated_at: DateTimeField representing the last update timestamp.
    - updated_by: ForeignKey to BaseUser or None, representing the user
                who last updated the instance.

    Note: This model is abstract and serves as a base for other models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    created_by: models.ForeignKey[BaseUserOrNone, Optional['BaseUser']] = (
        models.ForeignKey(
            to=AUTH_USER_MODEL, editable=False, on_delete=models.SET_NULL, null=True,
            related_name='+'
        )
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by: models.ForeignKey[BaseUserOrNone, Optional['BaseUser']] = (
        models.ForeignKey(
            to=AUTH_USER_MODEL, editable=False, on_delete=models.SET_NULL, null=True,
            related_name='+'
        )
    )

    class Meta:
        abstract = True

    def get_related_names(self) -> RelatedNames:

        """
        Get related names for created and updated fields.

        :returns: RelatedNames: A dictionary containing related names
        for created and updated fields.
        """

        return {
            'created': f'%(app_label)s_{self.__class__.__name__.lower()}_created',
            'updated': f'%(app_label)s_{self.__class__.__name__.lower()}_updated',
        }

    def save(self, *args: Any, **kwargs: Any) -> None:

        """
        Save method overridden to set related names for created and updated fields.

        :params: *args: Variable length argument list.
        :params: **kwargs: Arbitrary keyword arguments.
        """

        if not self.pk:  # Only set related names for new instances
            related_names = self.get_related_names()

            if self.created_by is not None:
                # flake8: noqa B010

                setattr(self.created_by, 'related_name', related_names['created'])
                self.created_by.save()

            if self.updated_by is not None:
                # flake8: noqa B010

                setattr(self.updated_by, 'related_name', related_names['updated'])
                self.updated_by.save()

        super().save(*args, **kwargs)


class RandomModel(BaseModel):

    """
    This is an example model, to be used as a reference in the Styleguide,
    when discussing model validation via constraints.
    """

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
