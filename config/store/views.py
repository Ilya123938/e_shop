

from django.shortcuts import render, get_object_or_404,redirect
from .models import Product, Category
from .forms import ContactForm



from django.core.cache import cache
from django.core.paginator import Paginator

def product_list(request):

    products = cache.get('available_products')
    categories = cache.get('all_categories')

    if not products:
        products = Product.objects.filter(is_available=True)
        cache.set('available_products', products, 60)  # 60 ثانية

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    if not categories:
        categories = Category.objects.all()
        cache.set('all_categories', categories, 60)  # 60 ثانية
    
    
    
    paginator = Paginator(products, 3)  # 10 منتجات في الصفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    current_products = page_obj.object_list
  

    return render(request, 'pages/product_list.html', {
        'products': current_products,
        'categories': categories,
        'page_obj': page_obj,
        'selected_category': int(category_id) if category_id else None,  # نرسل الفئة المحددة للتمبليت

    })

def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(
        category=category,
        is_available=True
    )

    categories = Category.objects.all()

    return render(request, 'pages/product_list.html', {
        'category': category,
        'products': products,
        'categories': categories
    })


def product_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query, is_available=True)
    categories = Category.objects.all()

    return render(request, 'pages/product_search.html', {
        'products': products,
        'categories': categories,
        'query': query
    })

def product_details(request, id):
    product = get_object_or_404(Product, id=id, is_available=True)
    categories = Category.objects.all()

    return render(request, 'pages/product_details.html', {
        'product': product,
        'categories': categories
    })

def about(request):
    return render(request, 'pages/about.html')

from django.shortcuts import render

def contact(request):
    if request.method == "POST":
     form = ContactForm(request.POST)
     if form.is_valid():
        form.save()
        

        
        return redirect('store:contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})