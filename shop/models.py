import random
import string
from django.urls import reverse
from django.db import models
from django.utils.text import slugify


def rand_slug():
    """
    Generates a random slug of length 3 using lowercase letters and digits.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


# Create your models here.
class Category(models.Model):
    """
    Represents a category with a name, parent category, URL slug, and creation date.
    """
    name = models.CharField('Категория', max_length=255, db_index=True)
    parent = models.ForeignKey( 'self', on_delete=models.CASCADE, related_name='children',
                               null=True, blank=True)
    slug = models.SlugField('URL', max_length=255, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        Return a string representing the full path to the current node, starting from the root.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Save the object with a generated slug if it doesn't have one already.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if not self.slug:
            self.slug = slugify(rand_slug() + '-picBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_list', kwargs={'slug': self.slug})


class Product(models.Model):
    """
    Represents a product with a category, title, brand, description, URL slug, price, image, availability, and creation/update dates.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Название', max_length=255)
    brand = models.CharField('Бренд', max_length=255)
    description = models.TextField('Описание')
    slug = models.SlugField('URL', max_length=255)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=99.99)
    image = models.ImageField('Изображение', upload_to='products/products/%Y/%m/%d', blank=True)
    available = models.BooleanField('Наличие', default=True)
    create_at = models.DateTimeField('Дата создания', auto_now_add=True)
    update_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})


class ProdictManager(models.Manager):
    """
    Return a filtered queryset of available Prodict instances.
    """

    def get_queryset(self):
        return super(ProdictManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    """
    Represents a proxy model for the Product model.
    """
    objects = ProdictManager()

    class Meta:
        proxy = True
