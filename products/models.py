from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='images/', default='def.png', null=True, blank=True)
    product_price = models.FloatField()
    product_details = models.TextField(max_length=300, default="Nike Shoe")

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_location = models.CharField(max_length=20, choices=(('inside_dhaka', 'Inside Dhaka'), ('outside_dhaka', 'Outside Dhaka')))

    def __str__(self):
        return f"Cart for {self.user}"

    @property
    def total_amount(self):
        # Calculate item total
        item_total = sum(item.total_price for item in self.cartitem_set.all())
        
        # Set delivery charge based on location
        delivery_charge = 80 if self.delivery_location == 'inside_dhaka' else 130

        # Return the total amount including delivery
        return item_total + delivery_charge
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} in cart"
    
    @property
    def total_price(self):
        return self.product.product_price * self.quantity
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_location = models.CharField(
        max_length=20,
        choices=(('inside_dhaka', 'Inside Dhaka'), ('outside_dhaka', 'Outside Dhaka'))
    )
    total_amount = models.FloatField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.product_name} (x{self.quantity}) in order {self.order.id}"