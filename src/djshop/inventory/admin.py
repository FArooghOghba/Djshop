from django.contrib import admin

from src.djshop.inventory.models import StockRecord


@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin[StockRecord]):

    list_display = (
        'product',
        'sku',
        'sale_price',
    )
    search_fields = ('product__title', 'sku')
