from django.db import models
from django.contrib.auth.models import User

# Create your models here.



  
class AddToCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product_id=models.IntegerField()
    product_type=models.CharField(max_length=200)
    product_quantity=models.PositiveBigIntegerField(default=1)

    def _str_(self):
        return self.product_name


class Whishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product_id=models.IntegerField()
    product_type=models.CharField(max_length=200)



 




  















class Laptops(models.Model):
    laptop_name=models.CharField(max_length=200)
    laptop_description=models.TextField()
    laptop_price=models.DecimalField(max_digits=10,decimal_places=2)
    laptop_rating=models.CharField(max_length=200)
    laptop_image=models.ImageField(upload_to='laptops/')


    def __str__(self):
        return self.laptop_name



class Mobiles(models.Model):
    mobile_name=models.CharField(max_length=200)
    mobile_description=models.TextField()
    mobile_price=models.DecimalField(max_digits=10,decimal_places=2)
    mobile_rating=models.CharField(max_length=200)
    mobile_image=models.ImageField(upload_to='mobiles/')


    def __str__(self):
        return self.mobile_name


class Shoes(models.Model):
    shoe_name=models.CharField(max_length=200)
    shoe_description=models.TextField()
    shoe_price=models.DecimalField(max_digits=10,decimal_places=2)
    shoe_rating=models.CharField(max_length=200)
    shoe_image=models.ImageField(upload_to='shoes/')


    def __str__(self):
        return self.shoe_name

class Formal_Shoes(models.Model):
    shoe_name=models.CharField(max_length=200)
    shoe_description=models.TextField()
    shoe_price=models.DecimalField(max_digits=10,decimal_places=2)
    shoe_rating=models.CharField(max_length=200)
    shoe_image=models.ImageField(upload_to='formal_shoes/')


    def __str__(self):
        return self.shoe_name





class Shirt(models.Model):
    shirt_name=models.CharField(max_length=200)
    shirt_description=models.TextField()
    shirt_price=models.DecimalField(max_digits=10,decimal_places=2)
    # shirt_size=models.CharField(max_length=200)
    shirt_image=models.ImageField(upload_to='shirt/')


    def __str__(self):
        return self.shirt_name



class Television(models.Model):
    television_name=models.CharField(max_length=200)
    television_description=models.TextField()
    television_price=models.DecimalField(max_digits=10,decimal_places=2)
    television_rating=models.CharField(max_length=200)
    television_image=models.ImageField(upload_to='television/')


    def __str__(self):
        return self.television_name


class Jeans(models.Model):
    jeans_name=models.CharField(max_length=200)
    jeans_description=models.TextField()
    jeans_price=models.DecimalField(max_digits=10,decimal_places=2)
    # television_rating=models.CharField(max_length=200)
    jeans_image=models.ImageField(upload_to='jeans/')


    def __str__(self):
        return self.jeans_name

#grinders 
class Kitchen(models.Model):
    kitchen_name=models.CharField(max_length=200)
    kitchen_description=models.TextField()
    kitchen_price=models.DecimalField(max_digits=10,decimal_places=2)
    kitchen_rating=models.CharField(max_length=200)
    kitchen_image=models.ImageField(upload_to='kitchen/')


    def __str__(self):
        return self.kitchen_name

class Rice_cookers(models.Model):
    rice_cooker_name=models.CharField(max_length=200)
    rice_cooker_description=models.TextField()
    rice_cooker_price=models.DecimalField(max_digits=10,decimal_places=2)
    rice_cooker_rating=models.CharField(max_length=200)
    rice_cooker_image=models.ImageField(upload_to='rice_cooker/')


    def __str__(self):
        return self.rice_cooker_name


    
class Furniture(models.Model):
    furniture_name=models.CharField(max_length=200)
    furniture_description=models.TextField()
    furniture_price=models.DecimalField(max_digits=10,decimal_places=2)
    furniture_rating=models.CharField(max_length=200)
    furniture_image=models.ImageField(upload_to='furniture/')


    def __str__(self):
        return self.furniture_name

class Table(models.Model):
    furniture_name=models.CharField(max_length=200)
    furniture_description=models.TextField()
    furniture_price=models.DecimalField(max_digits=10,decimal_places=2)
    furniture_rating=models.CharField(max_length=200)
    furniture_image=models.ImageField(upload_to='table/')


    def __str__(self):
        return self.furniture_name


class Beauty(models.Model):
    furniture_name=models.CharField(max_length=200)
    furniture_description=models.TextField()
    furniture_price=models.DecimalField(max_digits=10,decimal_places=2)
    furniture_rating=models.CharField(max_length=200)
    furniture_image=models.ImageField(upload_to='beauty/')


    def __str__(self):
        return self.furniture_name



