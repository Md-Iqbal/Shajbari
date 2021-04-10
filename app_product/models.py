from django.db import models
from django.utils.safestring import mark_safe 
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.db.models import Avg, Count
# Create your models here.


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='Children')
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to='uploads/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True) 
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        full_path = [self.title]
        k =  self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])
    
    

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='uploads/')
    price = models.FloatField()
    amount = models.IntegerField()
    min_amount = models.IntegerField()
    details = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # create a fake table field in read only mode
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    
    image_tag.sort_description = 'Image'

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    
    def avaregereview(self):
        reviews = Comment.objects.filter(
            product=self).aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(
            product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

class GalleryImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='gallery/')

    def __str__(self):
        return self.title+" of -->"+self.product.title
    

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=500, blank=True)
    rate = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
