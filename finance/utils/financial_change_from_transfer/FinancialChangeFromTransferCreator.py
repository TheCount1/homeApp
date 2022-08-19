from finance.models import Transfer, FinancialChange, AssetType, Category


class FinancialChangeFromTransferCreator:
    def __init__(self, form_post):
        self.name = form_post['name']
        self.category = form_post['category']
        self.status = form_post['status']
        self.transfer_pk = form_post['transfer_pk']

    def set_transfer_status(self):
        transfer = Transfer.objects.get(pk=self.transfer_pk)
        transfer.status = self.status
        transfer.save()

    def insert_new_financial_change(self):
        transfer = Transfer.objects.get(pk=self.transfer_pk)
        financial_change = FinancialChange()
        financial_change.name = self.name
        financial_change.direction = transfer.direction
        financial_change.amount_gr = transfer.amount_gr
        financial_change.account = transfer.inner_account
        financial_change.date = transfer.posting_date
        financial_change.asset_type = AssetType.objects.get(name='Pieniądze')
        financial_change.category = Category.objects.get(name=self.category)
        financial_change.save()
        transfer.financial_change = financial_change
        transfer.save()
