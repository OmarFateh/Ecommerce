from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


def product_image(instance, filename):
    """
    Upload the product image into the path and return the uploaded image path.
    """   
    return f'products/{instance.variation.product.name}-{instance.variation.color.name}-{instance.variation.size.name}/{filename}'

class BaseTimestamp(models.Model):
    """
    Timestamp abstract model.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class ProductFavourite(BaseTimestamp):
    """
    A relationship model between the product and its favourites.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class ProductManager(models.Manager):
    """
    Product model manager.
    """
    def get_descendants_products(self, category, ids=None):
        """
        Take category, and get all products of descendants categories of this category.
        If ids is given, get all products ids of descendants categories of this category.
        """
        if ids:
            return self.get_queryset().filter(category__in=category.get_descendants(include_self=True)).values_list('id', flat=True).distinct()
        else:
            return self.get_queryset().filter(category__in=category.get_descendants(include_self=True)) 


class Product(BaseTimestamp):
    """
    Product model.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.CharField(max_length=255)
    details = models.TextField()
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()
    category = models.ForeignKey('category.Category', related_name="products", on_delete=models.SET_NULL, null=True)
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favourites', blank=True, through=ProductFavourite)
    in_stock = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    objects = ProductManager()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return Product's name.
        return f"{self.name}"

    @property
    def actual_price(self):
        # Return sale price if exists and if not, get regular price of product's variation 
        if self.sale_price:
            return self.sale_price
        else:
            return self.regular_price 

    def get_price_sale_difference(self):
        if self.sale_price:
            # Return the difference between regular price and sale price.
            return self.regular_price - self.sale_price

    def get_price_sale_difference_precentage(self):
        if self.sale_price:
            # Return the precentage difference between regular price and sale price.
            return (self.get_price_sale_difference()*100)// self.regular_price     

    @property
    def get_absolute_url(self):
        # Return absolute url of product detail by its slug.
        return reverse("product:product-detail", kwargs={"product_slug": self.slug})


class ProductImageManager(models.Manager):
    """
    Product Image model manager. 
    """
    def get_images_data(self, product_id):
        """
        Take product's id, and get all its images.
        """
        images_list = []
        images = self.get_queryset().filter(variation__product__id=product_id) 
        if images.exists():      
            for obj in images:
                images_data = {
                    'id':obj.id, 
                    'image':obj.image.url,
                    'is_thumbnail': obj.thumbnail,
                    'variation':{'id':obj.variation.id},
                    'product':{'id':obj.variation.product.id},
                    'color':{'id':obj.variation.color.id, 'name':obj.variation.color.name, 'code':obj.variation.color.code},
                    'size':{'id':obj.variation.size.id, 'name':obj.variation.size.name},
                }
                images_list.append(images_data)            
        return images_list 

    def get_thumbnails_list(self, images_qs, thumbnail_url=None):
        """
        Take a queryset of images, and return first two of its thumbnails urls.
        """
        thumbnails_list = []
        if thumbnail_url:
            thumbnails_list.append(thumbnail_url)
        for obj in images_qs:
            if obj.image.url not in thumbnails_list and not len(thumbnails_list) > 2:
                thumbnails_list.append(obj.image.url)
        return thumbnails_list         

    def get_thumbnails(self, product_id):
        """
        Take product's id, and get first two of its thumbnails.
        """
        thumbnails = self.get_queryset().filter(variation__product__id=product_id, thumbnail=True) 
        if thumbnails.count() > 1: 
            return self.get_thumbnails_list(thumbnails)        
        images = self.get_queryset().filter(variation__product__id=product_id) 
        if thumbnails.count() == 1:
            thumbnails_list = self.get_thumbnails_list(images, thumbnail_url=thumbnails.first().image.url)
        elif not thumbnails.exists():
            thumbnails_list = self.get_thumbnails_list(images)
        return thumbnails_list

    def get_favourite_list_thumbnail(self, product_id):
        """
        Take product's id, and get its first thumbnail.
        """
        thumbnails = self.get_queryset().filter(variation__product__id=product_id, thumbnail=True)
        if thumbnails.exists():
            return thumbnails.first()
        else:
            return self.get_queryset().filter(variation__product__id=product_id).first()


class ProductImage(BaseTimestamp):
    """
    Product image model.
    """
    variation = models.ForeignKey('Variation', related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    objects = ProductImageManager()

    class Meta:
        ordering = ['variation']

    def __str__(self):
        # Return variation.
        return f"{self.variation}"


class ProductColor(BaseTimestamp):
    """
    Product color model.
    """
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16)

    class Meta:
        ordering = ['name']

    def __str__(self):
        # Return color's name.
        return f"{self.name}"


class ProductSize(BaseTimestamp):
    """
    Product size model.
    """
    name = models.CharField(max_length=64)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        # Return size's name.
        return f"{self.name}"


class VariationManager(models.Manager):
    """
    Variation model manager. 
    """
    def get_size_color_list(self, product_id, size_id=None):
        """
        Take product's id and size's id, and get list all colors of these size and product.
        """
        list_data= []
        if size_id:
            variations_color = self.get_queryset().filter(product__id=product_id, size__id=size_id).order_by("size")
            if variations_color.exists():
                for obj in variations_color:
                    color_data = {'id':obj.color.id, 'name':obj.color.name, 'code':obj.color.code}
                    if color_data not in list_data:
                        list_data.append(color_data)            
        return list_data 

    def get_product_sizes(self, product_id):
        """
        Take product's id, and get all unduplicated sizes of this product.
        """
        size_list = []
        product_sizes = self.get_queryset().filter(product__id=product_id).order_by("size")
        for obj in product_sizes:
            size_data = {'id':obj.size.id, 'name':obj.size.name}
            if size_data not in size_list:
                size_list.append(size_data)            
        return size_list 

    def get_category_products_sizes(self, category):
        """
        Take category, and get all unduplicated sizes of all products of this category.
        """
        products_ids = Product.objects.get_descendants_products(category=category, ids=True)
        return self.get_queryset().filter(product__id__in=products_ids).order_by('size').values(
            'size__id', 'size__name'
        ).distinct()      

    def get_category_products_colors(self, category):
        """
        Take category, and get all unduplicated colors of all products of this category.
        """
        products_ids = Product.objects.get_descendants_products(category=category, ids=True)
        return self.get_queryset().filter(product__id__in=products_ids).order_by('color').values(
            'color__id', 'color__name', 'color__code'
        ).distinct()                 

    def get_variation_data(self, product_id):
        """
        Take product's id, and get all its variations.
        """
        variation_list = []
        variations = self.get_queryset().filter(product__id=product_id).order_by("size")        
        for obj in variations:
            variation_data = {
                'id':obj.id, 
                'product':{'id':obj.product.id},
                'color':{'id':obj.color.id, 'name':obj.color.name, 'code':obj.color.code},
                'size':{'id':obj.size.id, 'name':obj.size.name},
            }
            variation_list.append(variation_data)            
        return variation_list    

    def get_products_ids(self, products_variation):
        """
        Take products variation, and get all its products' ids.
        """
        products_ids = []
        if products_variation:
            for obj in products_variation:
                if obj.product.id not in products_ids:
                    products_ids.append(obj.product.id) 
        return products_ids   
       

class Variation(BaseTimestamp):
    """
    Product variation model.
    """
    product = models.ForeignKey(Product, related_name="variations", on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, related_name="colors", on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, related_name="sizes", on_delete=models.CASCADE)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    objects = VariationManager()

    class Meta:
        unique_together = ['product', 'color', 'size']
        ordering = ['-created_at']

    def __str__(self):
        # Return Product's name, color's name, and size's name.
        return f"{self.product.name} | {self.color.name} | {self.size.name}"

    @property
    def first_image(self):
        #  Return first image of a variation.
        return self.images.first()

    @property
    def actual_price(self):
        # Return sale price if exists and if not, get regular price of product's variation 
        if self.sale_price:
            return self.sale_price
        else:
            return self.regular_price        


class ProductReview(BaseTimestamp):
    """
    Product review model.
    """
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    rate = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        # Return Product's name, user's name and his rate.
        return f"{self.product.name} | {self.user.first_name} {self.user.last_name} | {self.rate} stars"

    def get_update_delete_absolute_url(self):
        # Return absolute url of update and delete review by its id.
        return reverse('accounts:update-delete-review', kwargs={'review_id': self.pk})

    def get_rate_precentage(self):
        # Return review rate precentage.
        return (self.rate * 20)        