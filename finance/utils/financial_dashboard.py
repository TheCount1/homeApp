from finance import models


# TODO Split function into parts?

def get_wealth_sum(owner):
    financial_changes = models.FinancialChange.objects.filter(account__owner='A')
    wealth_sum = 0
    for financial_change in financial_changes:
        if financial_change.direction == "I":
            wealth_sum += financial_change.amount_gr
        elif financial_change.direction == "O":
            wealth_sum -= financial_change.amount_gr
    return wealth_sum


def get_current_cash():
    financial_changes = models.FinancialChange.objects.all()
    cash_sum = 0
    cash_asset_type = models.AssetType.objects.get(name='Pieniądze')
    for financial_change in financial_changes:
        if financial_change.asset_type == cash_asset_type:
            if financial_change.direction == "I":
                cash_sum += financial_change.amount_gr
            elif financial_change.direction == "O":
                cash_sum -= financial_change.amount_gr
    return cash_sum
