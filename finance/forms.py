from django import forms
from django.forms import DateInput

from . import models


class ImportTransfersForm(forms.Form):
    import_file = forms.FileField()


def get_category_choices():
    categorys = models.Category.objects.all()
    category_choices = []
    for cat in categorys:
        new_choice = (cat.name.__str__(), cat.name.__str__())
        category_choices.append(new_choice)
    return category_choices


def get_status_choices():
    status_choices = []
    statuses = models.Transfer.STATUSES


class FinancialChangeForm(forms.Form):
    name = forms.CharField()
    category = forms.ChoiceField(choices=get_category_choices())
    status = forms.ChoiceField(choices=models.Transfer.STATUSES, widget=forms.RadioSelect)










"""  date = forms.DateField(widget=forms.DateInput())"""

"""    date = forms.DateField(null=True)
    direction = forms.ChoiceField(max_length=1, choices=DIRECTIONS)
"""

"""   account = forms.ChoiceField(choices=models.Account.all())
   asset_type = forms.ForeignKey(AssetType, null=True, on_delete=models.SET_NULL)
   category = forms.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
"""

"""  DIRECTIONS = (
      ('I', 'Incoming'),
      ('O', 'Outgoing')
  )
  name = models.CharField(max_length=255)
  amount_gr = models.DecimalField(max_digits=20, decimal_places=2)
  date = models.DateField(null=True)
  direction = models.CharField(max_length=1, choices=DIRECTIONS)
  account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
  asset_type = models.ForeignKey(AssetType, null=True, on_delete=models.SET_NULL)
  category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
"""