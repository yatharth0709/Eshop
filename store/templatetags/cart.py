from django import template #CREATING A FILTER OF OUR OWN

register=template.Library()#DECORATOR

@register.filter(name='isincart') #name specifies what name to call it with in the html
def isincart(product,cart):
    key=cart.keys()
    for id in key:
        if int(id)==product.id:
            return True
    return False

@register.filter(name='cartquant') #name specifies what name to call it with in the html
def cartquant(product,cart):
    key=cart.keys()
    for id in key:
        if int(id)==product.id:
            return cart.get(id)
    return 0

@register.filter(name="pricetotal")
def pricetotal(product,cart):
    return product.price * cartquant(product,cart)


@register.filter(name="totalcartprice")
def totalcartprice(products,cart):
    sum = 0;
    for p in products:
        sum+=pricetotal(p, cart)    
    return sum

@register.filter(name="currency")
def currency(number):
    return "₹"+str(number)

@register.filter(name="multiply")
def multiply(number,number1):
    return number*number1

