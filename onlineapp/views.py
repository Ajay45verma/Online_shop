from django.shortcuts import render,redirect
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.shortcuts import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
def index(request):
   if request.method=="GET": 
      
     products=None
     categories=Category.get_all_Category()
     categoryID=request.GET.get('category')
   # print(categoryID)
     if categoryID:
        products=Product.get_all_products_by_category(categoryID)
     else:
         products=Product.get_all_products()
     data={
        'products':products,
        'categories':categories
    }
     print('my email', request.session.get('customer_email'))
     return render(request, 'index.html',data)
   else:
     cart_id=request.POST.get("cart_product")
     cart=request.session.get('cart')
     if cart:
        quantity=cart.get(cart_id)
        if quantity:
           cart[cart_id]=quantity+1
        else:
            cart[cart_id]=1

     else:
        cart={}
        cart[cart_id]=1
     request.session['cart']=cart
     print(request.session['cart'])

     return redirect("homepage")

#sign up page start here

def signup(request):
    if request.method=="POST":
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        value={
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email
        }
        customer=Customer(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                password=password
                             )
#form validation start here
        error_message=None
        if cpassword!=password:
            error_message="Your Password did not matched"
        elif not first_name:
            error_message="First Name Required"
        elif len(first_name)<3:
            error_message="First Name must be 3 char long or more"
        elif not last_name:
            error_message="Last Name Required"
        elif len(last_name)<3:
            error_message="Last name must be 3 character long or more"
        elif len(phone)<3 and len(phone)>15:
            error_message="Please Enter a Valid Phone Number"
        elif len(password)<4 and len(password)>20:
            error_message="Please Enter a valid Password"
        #CHECK EMAIL IS UNIQE OR NOT
        IsExist=customer.IsExist()
        if IsExist==True:
            error_message="Your Email Already Exist"
        #password hassing
        customer.password=make_password(customer.password)
    # saving customer form

        if not error_message:
             customer.save()
             return redirect('homepage')
        else:
            data={
                'error':error_message,
                'values':value
            }
            return render(request, 'signup.html', data)
    
    return render(request, 'signup.html')

def log(request):
    if request.method=='GET':
        return render(request, 'log.html')
    else:
        email=request.POST.get("lemail")
        password=request.POST.get("lpassword")
        err_massage=None
        customer=Customer.get_customerData_by_email(email)
        #print(customer)
        if customer:
            #print("yes")
            flag=check_password(password, customer.password)
           # print(flag)
            if flag:
                request.session['customer_id']=customer.id
                request.session['customer_email']=customer.email
                return redirect('homepage')
            else:
                err_massage="Plese enter valid password "
               # return render(request, 'log.html')

        else:
           # print("no")
           err_massage="invalid email"
        
        return render(request, 'log.html', {'error':err_massage})
       
     
        
        #print(email, password,isCustomer)