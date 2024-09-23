
from store.models import Product,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,get_object_or_404,redirect
from store.models import Product, Cart, CartItem
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from store.forms import CartForm, SearchForm,Orderform


# Create your views here.

def home(request):
    products=Product.objects.all()
    # cart=Cart.objects.get(user=request.user)
    # length=len(CartItem.objects.filter(cart=cart))
    category=Category.objects.all()
    return render(request,'home.html',{'products':products,'category':category})



def about(request):
    return render(request,'about.html',{})

def product_view(request,id):
    product=Product.objects.get(id=id)
    return render(request,'product.html',{'product':product})



def category(request,name):
    name=name.replace('-',' ')
    category=Category.objects.get(name=name)
    products=Product.objects.filter(category=category)
    return render(request,'category.html',{"products":products,"category":category})


def login_user(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'login.html',{'form':form})

def logout_user(request):
    logout(request)
    return redirect('home')


# def add_cart(request):
#     product=Product.objects.get(pk=pk1)
#     cart=Cart.objects.get_or_create(product=product)
    #total_price=cart.t
    
    #return render(request,'cart_summary.html',{}


# Create your views here.

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    t=len(cart_items)
    total_price = cart.total_price
    return render(request, 'cart_summary.html', {'cart_items': cart_items, 'total_price': total_price,'length':t})

@login_required
def add_to_cart(request, product_id):
    print(f"Adding product {product_id} to cart...")
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()
    cart.total_price += product.price * cart_item.quantity
    cart.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    cart = Cart.objects.get(user=request.user)
    cart.total_price -= cart_item.product.price * cart_item.quantity
    cart.save()
    return redirect('cart_view')

@login_required
def update_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    form = CartForm(request.POST or None, instance=cart_item)
    if form.is_valid():
        form.save()
        cart = Cart.objects.get(user=request.user)
        cart.total_price = sum([item.product.price * item.quantity for item in CartItem.objects.filter(cart=cart)])
        cart.save()
        return redirect('cart_view')
    return render(request, 'app1/update_cart.html', {'form': form, 'cart_item': cart_item})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html',{'form':form})

def search_view(request):
      form = SearchForm(request.GET or None)
      products = Product.objects.all()
      if form.is_valid():
        query = form.cleaned_data.get('query')

        if query:
            products = products.filter(name__icontains=query)

      return render(request, 'search.html',{'products':products})
  
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price
    
    form_data = None
    
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data  # Capture the cleaned data from the form
            form.save()
             
            # cart_items.delete()
            # cart.total_price=0
            # cart.save()
            
    else:
        form = Orderform()

    context = {
        'all_items': cart_items,
        'total_price': total_price,
        'form': form,
        'form_data': form_data,  # Pass the form data to the template
    }
   

    return render(request, 'checkout.html', context)