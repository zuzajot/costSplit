from django.contrib import admin
from .models import Profile, Group, GroupUser, CostUser, Cost, Payment, Currency, PaymentUser

# Register your models here.


admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(GroupUser)
admin.site.register(Cost)
admin.site.register(CostUser)
admin.site.register(Payment)
admin.site.register(Currency)
admin.site.register(PaymentUser)

