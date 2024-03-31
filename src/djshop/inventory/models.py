from django.db import models

from src.djshop.common.models import BaseModel


class StockRecord(BaseModel):
    product = models.ForeignKey(
        to='catalog.Product', on_delete=models.CASCADE, related_name='stock_records'
    )
    sku = models.CharField(max_length=64, unique=True, null=True, blank=True)
    buy_price = models.PositiveBigIntegerField(null=True, blank=True)
    sale_price = models.PositiveBigIntegerField()
    num_stock = models.PositiveIntegerField(default=0)
    threshold_low_stock = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Stock Record"
        verbose_name_plural = "Stock Records"

    def __str__(self) -> str:

        """
        Returns a human-readable string representation of the category.

        :returns: str: The title of the category.
        """

        return f'{self.product.title} >> {self.num_stock}'
