from django.db import models
from django.db.models import F, Q
from django.utils import timezone

from src.config.django.base import AUTH_USER_MODEL


class BaseModel(models.Model):

    """
    This is a base model, The fields of this model are probably used in all models.
    """

    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    created_by = models.ForeignKey(
        to=AUTH_USER_MODEL, editable=False, on_delete=models.SET_NULL, null=True,
        related_name='created'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        AUTH_USER_MODEL, editable=False, on_delete=models.SET_NULL, null=True,
        related_name='modified'
    )

    class Meta:
        abstract = True


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
