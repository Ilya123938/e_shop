from django.conf import settings
from store.models import Product
from decimal import Decimal
from coupons.models import Coupon


class CartConfig:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
       

    # إضافة منتج للسلة
    def add(self, product, quantity=1, overwrite_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if overwrite_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    # حفظ التغييرات
    def save(self):
        self.session.modified = True

    # حذف منتج
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # تكرار عناصر السلة
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # عدد العناصر في السلة
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # السعر الإجمالي
    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    # إنقاص الكمية
    def decrement(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1

            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product)
            else:
                self.save()
    @property
    def coupon(self):
        if self.coupon_id:
            try:
               return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def get_discount(self):
        if self.coupon:
            return(self.coupon.discount/ Decimal(100))*self.get_total_price()
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
    
    
    
    

    

  

    
        
   
            




    # إفراغ السلة
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
