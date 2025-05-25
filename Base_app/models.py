from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class itemList(models.Model):
    Category_name= models.CharField(max_length=15)

    def __str__(self):
        return self.Category_name
class items(models.Model):
    Item_name= models.CharField(max_length=15)
    description=models.TextField(blank=False)
    Price=models.IntegerField()
    Category=models.ForeignKey(itemList,related_name='Name',on_delete=models.CASCADE)
    Image=models.ImageField(upload_to='Items/')

    def __str__(self):
        return self.Item_name
    
class AboutUs(models.Model):
    Description=models.TextField(blank=False)
class Feedback(models.Model):
    User_name=models.CharField(max_length=15)
    Description=models.TextField(blank=False)
    Rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    Image=models.ImageField(upload_to='Items/',blank=True)

    def __str__(self):
        return self.User_name
    

class BookTable(models.Model):
    Name=models.CharField(max_length=15)
    Phone_number=models.IntegerField()
    Email=models.EmailField()
    Total_person=models.IntegerField()
    Booking_date=models.DateField()

    def __str__(self):
        return self.Name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(items, on_delete=models.CASCADE)  # Change from CharField
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.Item_name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)  
    address = models.TextField()
    phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Set default value
    status = models.CharField(default="Processing", max_length=20)
    ordered_at = models.DateTimeField(auto_now_add=True)













