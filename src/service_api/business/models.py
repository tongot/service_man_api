import uuid
from django.db import models
from datetime import datetime

def image_name_id(instance,filename):
        extension = filename.split(".")[-1]
        return "{}.{}".format(uuid.uuid4(),extension)

class BusinessCategory(models.Model):

    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255,blank=True, null=True)
    
    def __str__(self):
        return self.name

class ProductCategory(models.Model):

    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Location(models.Model):

    country = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return "{} {}".format(self.country,self.city)


class Business(models.Model):

    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255, blank=False)
    owner = models.ForeignKey('account_api.UserAccount' ,on_delete= models.CASCADE)
    address = models.CharField(max_length=255, blank=False)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    phone = models.CharField(max_length=15, blank=False)
    contact_persona_name = models.CharField(max_length=255, blank=False)
    contact_persona_phone = models.CharField(max_length=15)
    business_logo = models.ImageField('business logo',blank=True,null=True, upload_to=image_name_id)
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    category = models.ForeignKey(BusinessCategory, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class BusinessReviews(models.Model):
    """stores the comment passed by an individual for a product"""
      
    STARS=[ 
        ( 0,'NONE'),
        ( 1,'GOOD'),
        (2,'BETTER'),
        ( 3,'COOL'),
        ( 4,'BEST'),
        ( 5,'EXCELLENT')]

    comment = models.CharField(max_length=5000,blank=False)
    stars = models.IntegerField(choices=STARS,default=0,blank=True,null=True)
    user = models.ForeignKey('account_api.UserAccount',on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    


class BusinessCommentReply(models.Model):
    """Business comment replies are stored here"""
    comment = models.CharField(max_length=5000,blank=False)
    business_comment = models.ForeignKey(BusinessReviews,on_delete= models.CASCADE)
    user = models.ForeignKey('account_api.UserAccount',on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)


class Product(models.Model):

    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255, blank=False)
    price = models.DecimalField(max_digits=20,blank=False, decimal_places=2)
    quantity = models.IntegerField(blank=False)
    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    product_new = models.BooleanField(default=1)
    product_available = models.BooleanField(default=0)
    price_neg =  models.BooleanField(default=0)
    business = models.ForeignKey(Business,on_delete= models.CASCADE)
    
    def __str__(self):
        return self.name


class ProductImages(models.Model):
    image = models.ImageField('product image',blank= True, null =True,  upload_to=image_name_id)
    product = models.ForeignKey(Product, related_name='product_images' ,on_delete= models.CASCADE)
    is_cover = models.BooleanField(default=0)


class OtherProductProperty(models.Model):
    """Other properties that a broduct mighgt have worth mentioning by the seller"""
    property_name = models.CharField(max_length=255,blank=False)
    description = models.CharField(max_length=400, blank=False)
    product = models.ForeignKey(Product,related_name='other_properties', on_delete= models.CASCADE)


class ProductReviews(models.Model):
    """stores the comment passed by an individual for a product"""
    STARS=[ 
        ( 0,'NONE'),
        ( 1,'GOOD'),
        (2,'BETTER'),
        ( 3,'COOL'),
        ( 4,'BEST'),
        ( 5,'EXCELLENT')]
    comment = models.CharField(max_length=5000,blank=False)
    stars = models.IntegerField(choices=STARS, default=0,blank=True,null=True)
    user = models.ForeignKey('account_api.UserAccount',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductCommentReply(models.Model):
    """Business comment replies are stored here"""
    comment = models.CharField(max_length=5000,blank=False)
    product_comment = models.ForeignKey(ProductReviews,on_delete= models.CASCADE)
    user = models.ForeignKey('account_api.UserAccount',on_delete=models.CASCADE)

 
class Service(models.Model):

    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255, blank=False)
    business = models.ForeignKey(Business,on_delete= models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    """change these defaults wen time to move database"""

    YES='YES'
    NO='NO'
    APPROVAL_STATE=[
        (YES,'YES'),
        (NO,'NO'),
    ]
    country = models.CharField(max_length=255,blank=False)
    first_name =  models.CharField(max_length=255,blank=False)
    last_name =  models.CharField(max_length=255,blank=False)
    street_address =  models.CharField(max_length=255,blank=False)
    street_address2 =  models.CharField(max_length=255,blank=False)
    email_address =  models.CharField(max_length=255,blank=False)
    phone_number = models.CharField(max_length=255,blank=False)
    customer = models.IntegerField(blank=True,null=True)
    quantity = models.IntegerField(blank=False,default=1)
    date_of_order = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete= models.DO_NOTHING)
    business = models.ForeignKey(Business,blank=True,null=True,on_delete=models.DO_NOTHING)
    approved = models.CharField(max_length=3, choices=APPROVAL_STATE,default=NO)
    viewed = models.BooleanField(default=False)



class TypeOfGoodsSold(models.Model):

    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)


class Message(models.Model):

    text = models.CharField(max_length=255,blank=False,null=False)
    phone = models.CharField(max_length=255,blank=False,null=False)
    email = models.EmailField(blank=True, null=True)
    customer = models.IntegerField(blank=True,null=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    product = models.IntegerField(blank=True, null=True)
    
