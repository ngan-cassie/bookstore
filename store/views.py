from django.shortcuts import render, get_object_or_404
from .models import Category, Product
# Create your views here.
# Connect everything up in the project 

def categories(request):
    return {
        'categories': Category.objects.all()
    }
def all_products(request): 
    # grab data and show them to the homepage
    products = Product.objects.all() # select all from product table -> save into products variable
    return render(request, 'store/home.html', {'products': products}) 
                        # template to use     # data to display on that template

def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug, in_stock = True) 
    return render(request, 'store/products/detail.html', {'product': product})

def category_list(request, category_slug):
    # ... /search/cooking
    category = get_object_or_404(Category, slug = category_slug)
    products = Product.objects.filter(category = category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})
                        
                    


