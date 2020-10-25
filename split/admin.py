from django.contrib import admin
from .models import Profile, Group, GroupUser, CostUser, Cost, Payment

# Register your models here.

admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(GroupUser)
admin.site.register(Cost)
admin.site.register(CostUser)
admin.site.register(Payment)
