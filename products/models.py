from django.db import models
from django.db.models import Q
class ProductManager(models.Manager):
    def with_text(self, text):
        queryset = self.get_queryset().filter(name__contains = text)
        return queryset
    
    def expensive_products(self):
        return self.get_queryset().filter(price__gte = 140)
    
    def cheap_toys(self):
        return self.get_queryset().filter(category__name='Category2', price__lte=100)
    
    def toys_or_expensive_items(self):
        query_filter = Q(category__name = 'Category2') | Q(price__gte = 140)
        queryset = self.get_queryset().filter(query_filter)
        print(queryset.query)
        return queryset
        

# Create your models here.
class Category(models.Model):
    name = models.CharField('Nome', max_length = 50)
    description = models.TextField('Descrição')
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return (f'{self.name} - {self.products.count()}')

class Product(models.Model):
    objects = ProductManager()
    name = models.CharField('Nome', max_length = 100)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits = 8, decimal_places = 2)
    category = models.ForeignKey(
        Category, 
        on_delete = models.deletion.DO_NOTHING,
        related_name ='products' # relaciona 'products' a todos os produtos da categoria
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField('Nome do Cliente', max_length = 100)
    payment = models.CharField('Forma de Pagamento', max_length = 50)
    products = models.ManyToManyField(Product)

    @property
    def total_amount(self):
        return sum([product.price for product in self.products.all()])
    
    def __str__(self):
        return f'{self.name} - R$ {self.total_amount}'
