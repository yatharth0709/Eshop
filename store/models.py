from django.db import models
from django.utils import timezone
# Create your models he
class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name
    @staticmethod
    def collectall():
        return Category.objects.all()

    

class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    description=models.CharField(max_length=200,default='',null=True,blank=True)
    Category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    image=models.ImageField(upload_to='uploads/products/',default='')
    def __str__(self):
        return self.name

    @staticmethod
    def getallproducts():
        return Product.objects.all()
    
    @staticmethod
    def collectbycategoryid(category_id):
        if(category_id):
            return Product.objects.filter(Category_id=category_id)
        else:
            return collectall()

    @staticmethod
    def getprbyid(id):
        return Product.objects.filter(id__in=id)



class Customer(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    phone=models.CharField(max_length=12)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=500)
    def __str__(self):
        return self.firstname

    def userregister(self):
        self.save()

    @staticmethod
    def getcustbyemail(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
    
    def isexists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False


class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=14,default='',blank=True)
    date = models.DateTimeField(default=timezone.now)
    status=models.BooleanField(default=False)
    
    def placeorder(self):
        self.save()
    
    @staticmethod
    def getordersbycust(customerid):
        return Order.objects.filter(customer=customerid).order_by('-date')