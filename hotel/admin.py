from django.contrib import admin
# Register your models here.
from .models import Room, Customer, Account, Order, Notice, OrderCustomerRoom
#

admin.site.register(Room)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Account)
admin.site.register(Notice)
admin.site.register(OrderCustomerRoom)
