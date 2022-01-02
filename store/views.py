from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from .models import Product,Category,Customer,Order
from django.contrib.auth.hashers import make_password ,check_password
from .forms import login,signup
from django.views import View
from store.middlewares.auth import loginmiddleware
import razorpay



class index(View):
    def get(self,request):
        prds= None
        cart=request.session.get('cart')
        if not cart:
            request.session.cart={}
  
        cats=Category.collectall()
        catid=request.GET.get('category')
        if catid:
            prds=Product.collectbycategoryid(catid)
        else: 
            prds=Product.getallproducts()
        return render(request,'index.html',{'products':prds,'Category':cats})
    
    def post(self,request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity==1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product]=quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart

        return redirect('homepage')

class SignupUser(View):
    def get(self,request):
        form=signup()    
        form.order_fields(field_order = ['firstname','lastname','email','password','phone'])
        return render(request,'signup.html',{'form':form})   
       
    def post(self,request):
         form=signup(request.POST)
         form.order_fields(field_order = ['firstname','lastname','email','password','phone'])
         error=None
         customer=Customer()
         customer.firstname=form.data['firstname']
         customer.lastname=form.data['lastname']
         customer.email=form.data['email']
         customer.password=form.data['password']
         customer.phone=form.data['phone']
         if customer.isexists():
            error="User Already Exists with this Email"
            return render(request,'signup.html',{'error':error,'form':form})
         else :
            customer.password=make_password(customer.password)
            customer.userregister()  #REMEMBER REGISTER LATER AFTER VALIDATION 
            return redirect('homepage') 

class Login(View):
    return_url=None

    def get(self,request):
        Login.return_url=request.GET.get('return_url')
        print("get",Login.return_url)
        form2=login()    
        form2.order_fields(field_order = ['email','password'])
        return render(request,'login.html',{'form':form2})
   
    def post(self,request):
            
            print("post",Login.return_url)
            form2=login(request.POST)
            form2.order_fields(field_order = ['email','password'])
            email=form2.data['email']
            password=form2.data['password']
            customer=Customer.getcustbyemail(email)
            errormsg=None
            if customer:
                flag=check_password(password,customer.password)
                print(flag)
                if flag:
                    request.session['customer']=customer.id
                    if Login.return_url:
                        return HttpResponseRedirect(Login.return_url)
                    else:
                        Login.return_nurl=None
                        return redirect('homepage')
                else:
                    errormsg='Email or Password invalid!!'
                
            else:   
                errormsg='Email or Password invalid!!'
            return render(request,'login.html',{'error':errormsg,'form':form2})

def logout(request):
    request.session.clear()
    return redirect('login')

class Cart(View):
    def get(self,request):
        id=list(request.session.get('cart').keys())
        products=Product.getprbyid(id)
        return render(request,'cart.html',{'products':products})

class Checkout(View):
    def post(self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        products=Product.getprbyid(list(cart.keys()))
        print(address,phone,customer,products)

        for product in products:
            order=Order(customer=Customer(id=customer),product=product,
            price=product.price,
            address=address,
            phone=phone,
            quantity=cart.get(str(product.id)))


        order.placeorder()
        request.session['cart']={} #clearing cart as order placed
        return render('cart')

class OrderView(View):
    
    def get(self,request):
        customer=request.session.get('customer')
        orders=Order.getordersbycust(customer)
        return render(request,'orders.html',{'orders':orders})

class payment(View):

    def get(self,request):
        keyid="rzp_test_ZpNruv2vDpktvI"
        keysecret="R7b4FUV7xebuzuMEWVXQWGky"

        client = razorpay.Client(auth=(keyid,keysecret))
        
        customer=request.session.get('customer')
        orders=Order.getordersbycust(customer)
        return render(request,'payment.html',{'orders':orders})

        order=client.order.create(data=data)
        print(order)
