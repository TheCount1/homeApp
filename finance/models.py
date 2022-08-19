from django.db import models


class Account(models.Model):
    OWNERS = (
        ('A', 'Adrian'),
        ('J', 'Asia')
    )
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    owner = models.CharField(max_length=1, choices=OWNERS)

    def __str__(self):
        return f'{self.get_owner_name()} {self.name}'

    def get_owner_name(self):
        for o in self.OWNERS:
            if o[0] == self.owner:
                return o[1]
        return 'Error'


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class AssetType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class FinancialChange(models.Model):
    DIRECTIONS = (
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

    def __str__(self):
        return f'financial change name {self.name} amount {self.amount_gr}'


class Reduction(models.Model):
    REDUCTION_TYPES = (
        ('B', 'Between Accounts'),
        ('R', 'Loan Return'),
        ('K', 'Brokerage')
    )

    type = models.CharField(max_length=1, choices=REDUCTION_TYPES)
    reductor = models.ForeignKey(FinancialChange, on_delete=models.CASCADE, related_name='reductor')
    reduced = models.ForeignKey(FinancialChange, on_delete=models.CASCADE, related_name='reduced')


class Transfer(models.Model):
    DIRECTIONS = (
        ('I', 'Incoming'),
        ('O', 'Outgoing')
    )
    STATUSES = (
        ('I', 'Inserted'),
        ('P', 'Postponed'),
        ('T', 'To insert')
    )
    sender_receiver = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    outer_account = models.CharField(max_length=30, null=True)
    operation_date = models.DateField(null=True)
    posting_date = models.DateField(null=True)
    description = models.CharField(max_length=255, null=True)
    amount_gr = models.DecimalField(max_digits=20, decimal_places=2)
    direction = models.CharField(max_length=1, choices=DIRECTIONS)
    status = models.CharField(max_length=1, choices=STATUSES, null=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    inner_account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    financial_change = models.ForeignKey(FinancialChange, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.direction == 'I':
            return f"incoming from {self.sender_receiver} amount {self.amount_gr} zl"
        else:
            return f"outgoing to {self.sender_receiver}  amount {self.amount_gr} zl"
