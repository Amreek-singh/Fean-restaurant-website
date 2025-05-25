from django.shortcuts import render,redirect
from Base_app.models import BookTable, AboutUs,Feedback,itemList,items,Order
# Create your views here.
from Base_app.models import BookTable
from .forms import BookTableForm,FeedbackForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages

def HomeView(request):
    Items=items.objects.all()
    list=itemList.objects.all()
    review=Feedback.objects.all()
    myform = BookTableForm()  # have added the form here because i also have book table in home

    message = None  # Initialize message variable

    if request.method == "POST":
        myform = BookTableForm(request.POST)
        if myform.is_valid():
            myform.save()
            message = "Your table is booked!"
            myform = BookTableForm()  # Reset the form after submission
        else:
            message = "Invalid input, please try again."
    return render(request,'home.html',{'Items':Items,'list':list,'review':review,'form':myform,'message':message})

def AboutView(request):
    return render(request,'about.html')

def MenuView(request):
    Items=items.objects.all()
    list=itemList.objects.all()
    return render(request,'menu.html',{'Items':Items,'list':list})

def BookTableView(request):
    message = None  
    
    if request.method == "POST":
        myform = BookTableForm(request.POST)
        if myform.is_valid():
            myform.save()
            message = "Your table is booked!" 
            myform = BookTableForm()
        else:
            message = "Invalid input, please try again."
    else:
        myform = BookTableForm()
        
    
    return render(request, 'book_table.html', {"form": myform, "message": message})
#def update(request,pk):
    
   # product=BookTable.objects.get(id=pk)
   # form=BookTableForm(instance=product)
   # if request.method=="POST":
        #form=BookTableForm(request.POST,instance=product)
    #    if form.is_valid():
    #        form.save()
   # return render(request,'book_table.html',{'form':form})

def feedback(request):
    message ="input is empty"
    if request.method == "POST":
        myfeedback=FeedbackForm(request.POST)
        if myfeedback.is_valid():
            myfeedback.save()
            return redirect('feedback')
    
        else:
            message = "Invalid input, please try again."
    else:
        myfeedback=FeedbackForm()   
       
    return render(request,'feedback.html',{"form": myfeedback,"message":message})

def read_more(request):
    return render(request,'Read_more.html')

def signup(request):
    if request.method=="POST":
       username=request.POST.get('username')
       email=request.POST.get('email')
       password=request.POST.get('password')
       confirm_password=request.POST.get('confirm_password')
       print(username,email,password,confirm_password)
       if password==confirm_password:
           if User.objects.filter(username=username).exists():
               return render(request,'signup.html',{'error':'user already exists'})
           else:
               user=User.objects.create_user(username=username,password=password,email=email)
               user.save()
               return render(request,"signup.html",{'error':"user created successfully"})
       else:
           return render(request,'signup.html',{'error':'password do not match'})
    return render(request,'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, "Successfully signed in!")
            return redirect('home')  # Redirect after login to clear the form
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'signin.html')

#def signout(request):
#    logout(request)
#    messages.info(request, "You are signed out!")  
#    return redirect('signin')
def signout(request):
    if  request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:  
            messages.error(request, "Please enter both username and password before signing out!")
        else:
            user = authenticate(request, username=username, password=password) #here it will check the valis enter users

            if user is not None:  # Only logout if valid credentials are entered
                logout(request)
                messages.info(request, "You are signed out!")
            else:
                messages.error(request, "Invalid user data, cannot sign out!")

    return redirect('signin')

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart,items


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(items, id=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=item)  # Store item itself, not name

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{item.Item_name} added to cart!")
    return redirect("menu")

def order_now(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request,'order_now.html',{"cart_items": cart_items})
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect("order_now")

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if request.method == "POST":
        address = request.POST["address"]
        phone = request.POST["phone"]
        
        # Calculate total price dynamically
        total_price = sum(item.product.Price * item.quantity for item in cart_items)

        order = Order.objects.create(user=request.user, address=address, phone=phone, total_price=total_price)
        order.items.set(cart_items)  # Add all cart items to the order
        cart_items.delete()  # Clear cart after placing order

        messages.success(request, f"Order placed successfully! Tracking ID: {order.id}")
        return redirect("order_status", order_id=order.id)  # Redirect to tracking page

    return render(request, "place_order.html", {"cart_items": cart_items})


@login_required
def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_status.html", {"order": order})

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "view_orders.html", {"orders": orders})
@login_required
def fake_payment(request):
    return render(request, "fake_payment.html")

