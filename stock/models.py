from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100, verbose_name="Назва категорії")
    description=models.TextField(blank=True, null=True, verbose_name="Опис")

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name=models.CharField(max_length=200, verbose_name="Назва товару")
    sku=models.CharField(max_length=50, unique=True, verbose_name="Артикул(SKU)")
    price=models.DecimalField(max_digits=10, decimal_places=2,  verbose_name="Ціна")
    quantity=models.IntegerField(default=0, verbose_name="Кількість на складі")
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")

    def __str__(self):
        return f"{self.name} ({self.sku})"