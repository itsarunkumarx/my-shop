from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (Category, Product,Customer, Order,OrderItem)
from .forms import ProductForm,RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Avg,Count, Sum
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

import traceback
from django.http import HttpResponse

def debug_view(request):
    try:
        cat_count = Category.objects.count()
        prod_count = Product.objects.count()
        prods = list(Product.objects.all()[:2])
        prod_info = [(p.name, str(p.image), getattr(p.image, 'url', None)) for p in prods]
        # Also test rendering home.html
        res = home(request)
        return HttpResponse(f"ALL OK! Categories: {cat_count}, Products: {prod_count}, Sample: {prod_info}, Home len: {len(res.content)}")
    except Exception:
        return HttpResponse(f"<h1>Error Traceback:</h1><pre>{traceback.format_exc()}</pre>", status=200)

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products
    }

    return render(request, 'home.html', context)


# Product List
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # -----------------------------
    # Search
    # -----------------------------
    search = request.GET.get("search")
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    # -----------------------------
    # Category Filter
    # -----------------------------
    category = request.GET.get("category")
    if category:
        products = products.filter(
            category_id=category
        )

    # -----------------------------
    # Price Filter
    # -----------------------------
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(
            price__gte=min_price
        )
    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    # -----------------------------
    # Sorting
    # -----------------------------
    sort = request.GET.get("sort")
    if sort == "low":
        products = products.order_by("price")
    elif sort == "high":
        products = products.order_by("-price")
    elif sort == "name":
        products = products.order_by("name")
    elif sort == "latest":
        products = products.order_by("-id")

    # -----------------------------
    # Pagination
    # -----------------------------
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    context = {
        "products": products,
        "categories": categories
    }

    return render(request, "product_list.html", context)

# Add Product
def product_add(request):

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product Added Successfully."
            )

            return redirect("product_list")

    else:

        form = ProductForm()

    return render(
        request,
        "product_form.html",
        {"form": form}
    )


# Update Product
def product_update(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product Updated Successfully."
            )

            return redirect("product_list")

    else:

        form = ProductForm(instance=product)

    return render(
        request,
        "product_form.html",
        {"form": form}
    )


# Delete Product
def product_delete(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product Deleted Successfully."
        )

        return redirect("product_list")

    return render(
        request,
        "product_delete.html",
        {"product": product}
    )
@login_required
def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')

def cart(request):

    cart = request.session.get('cart', {})

    cart_items = []

    total_price = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=int(product_id))

        subtotal = product.price * quantity

        total_price += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(
        request,
        'cart.html',
        context
    )
def increase_quantity(request, id):

    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:

        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')
def decrease_quantity(request, id):

    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:

        if cart[product_id] > 1:

            cart[product_id] -= 1

        else:

            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')
def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:

        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            messages.success(
                request,
                "Registration successful. Please login."
            )

            return redirect('login')

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )

def user_login(request):

    if request.method == "POST":

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login successful."
            )

            return redirect('profile')

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "login.html"
    )

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect('login')

@login_required
def profile(request):

    return render(
        request,
        "profile.html"
    )

@login_required
def checkout(request):

    return render(
        request,
        "checkout.html"
    )

@login_required
def place_order(request):

    if request.method != "POST":
        return redirect("checkout")

    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "state": request.POST.get("state"),
            "pincode": request.POST.get("pincode"),
        }
    )

    if not created:
        customer.phone = request.POST.get("phone")
        customer.address = request.POST.get("address")
        customer.city = request.POST.get("city")
        customer.state = request.POST.get("state")
        customer.pincode = request.POST.get("pincode")
        customer.save()

    order = Order.objects.create(
        customer=customer,
        total_amount=0
    )

    total = Decimal("0.00")

    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=int(product_id)
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        total += product.price * quantity

        product.stock -= quantity
        product.save()

    order.total_amount = total
    order.save()

    request.session["cart"] = {}

    messages.success(request, "Order placed successfully.")

    return redirect("my_orders")



@login_required
def my_orders(request):
    try:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer)
    except Customer.DoesNotExist:
        orders = []

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders
        }
    )
@login_required
def order_success(request, id):

    order = Order.objects.get(

        id=id

    )

    return render(

        request,

        "order_success.html",

        {

            "order": order

        }

    )

@login_required
def order_detail(request, id):

    order = Order.objects.get(

        id=id,

        customer__user=request.user

    )

    items = OrderItem.objects.filter(

        order=order

    )

    return render(

        request,

        "order_detail.html",

        {

            "order": order,

            "items": items

        }

    )

def product_detail(request, id):

    product = Product.objects.get(id=id)

    reviews = Review.objects.filter(
        product=product
    )

    average = reviews.aggregate(
        Avg("rating")
    )

    related_products = Product.objects.filter(

        category=product.category

    ).exclude(

        id=product.id

    )[:4]

    recent_products = Product.objects.order_by(

        "-id"

    )[:4]

    context = {

        "product": product,

        "reviews": reviews,

        "average": average,

        "related_products": related_products,

        "recent_products": recent_products

    }

    return render(

        request,

        "product_detail.html",

        context

    )

@login_required
def add_review(request, id):

    product = Product.objects.get(id=id)

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.product = product

            review.user = request.user

            review.save()

            return redirect(

                "product_detail",

                id=id

            )

    else:

        form = ReviewForm()

    return render(

        request,

        "review_form.html",

        {

            "form": form,

            "product": product

        }

    )

@staff_member_required
def admin_dashboard(request):

    # Total Products
    total_products = Product.objects.count()

    # Total Categories
    total_categories = Category.objects.count()

    # Total Users
    total_users = User.objects.count()

    # Total Orders
    total_orders = Order.objects.count()

    # Pending Orders
    pending_orders = Order.objects.filter(
        status="Pending"
    ).count()

    # Delivered Orders
    delivered_orders = Order.objects.filter(
        status="Delivered"
    ).count()

    # Low Stock Products
    low_stock_products = Product.objects.filter(
        stock__lte=5
    )

    low_stock_count = low_stock_products.count()

    # Recent Orders
    recent_orders = Order.objects.order_by(
        "-created_at"
    )[:5]

    # Total Sales
    total_sales = Order.objects.filter(
        status="Delivered"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    context = {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_users": total_users,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "low_stock_products": low_stock_products,
        "low_stock_count": low_stock_count,
        "recent_orders": recent_orders,
        "total_sales": total_sales,
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )