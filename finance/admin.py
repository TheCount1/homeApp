from django.contrib import admin
from . import models
from finance.models import FinancialChange, Category, Account, AssetType, Transfer, Reduction
# Register your models here.

admin.site.register(FinancialChange)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(AssetType)
admin.site.register(Transfer)
admin.site.register(Reduction)