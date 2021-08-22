# model the basket
# add functionalities to this basket
from store.models import Product
from decimal import Decimal

class Basket():
    """
    A base Basket class, providing some default behaviours that can be
    inherited or overrided, as necessary
    """

    def __init__(self, request):
        # build a session
        self.session = request.session
        # get the session key - reference point to name the cookie 
        basket = self.session.get('skey') 
        if 'skey' not in request.session:
            # set up a new session
            basket = self.session['skey'] = {} 
        self.basket = basket  
    
    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)
        print(product_id)
        if product_id not in self.basket: 
            self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)} # int: will round down 
        else:
            self.basket[product_id]['qty'] += qty
        # Tell Django that we modified the session 
        self.save()
        return product_id 

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database 
        and return products 
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in =product_ids) # if the current id is in product_ids
        basket = self.basket.copy() # copy an instance of our session data 

        for product in products:
            basket[str(product.id)]['product'] = product
        
        for item in basket.values():
            # convert string into decimal value
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty'] # add new key: total_price 
            yield item # return item 

    def __len__(self):
        """
        Get the basket data and count the quantity of items 
        """
        return sum(item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price'])*item['qty'] for item in self.basket.values())

    def delete(self, product):
        """
        find the item in the basket and delete it from session data
        """
        product_id = str(product) 
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()
    
    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty 

        self.save() 


    def save(self):
        self.session.modified = True 


# Check session id updates
# python3 manage.py shell
# >>> from django.contrib.sessions.models import Session
# >>> s = Session.objects.get(pk = '[ss_id]') 
# >>> s.get_decoded()
        