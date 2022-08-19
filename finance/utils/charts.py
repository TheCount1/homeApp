import decimal

from finance.models import FinancialChange, Category, AssetType

months_dict = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}


def get_summary_chart_data():
    time_labels = get_time_labels()
    summary_data = get_zeroed_data_set(time_labels)
    financial_changes = FinancialChange.objects.all()
    for financial_change in financial_changes:
        index = get_data_set_index(financial_change.date, time_labels)
        if financial_change.direction == 'I':
            summary_data[index] += financial_change.amount_gr
        else:
            summary_data[index] -= financial_change.amount_gr
    monthly_change = summary_data.copy()
    sum_accumulation(summary_data)
    charts_data = {'time_labels': time_labels, 'sum_values': summary_data, 'monthly_change': monthly_change}
    return charts_data


def get_income_expenses_chart_data():
    time_labels = get_time_labels()
    income_data = get_zeroed_data_set(time_labels)
    expenses_data = get_zeroed_data_set(time_labels)
    financial_changes = FinancialChange.objects.all()
    cash_asset_type = AssetType.objects.get(name='Pieniądze')
    for financial_change in financial_changes:
        index = get_data_set_index(financial_change.date, time_labels)
        if financial_change.direction == 'I' and financial_change.asset_type == cash_asset_type:
            income_data[index] += financial_change.amount_gr
        elif financial_change.asset_type == cash_asset_type:
            expenses_data[index] -= financial_change.amount_gr
    time_labels.pop(0)
    income_data.pop(0)
    expenses_data.pop(0)
    charts_data = {'time_labels': time_labels, 'income_values': income_data, 'expenses_values': expenses_data}
    return charts_data


def get_financial_change_monthly_sum_by_category():
    time_labels = get_time_labels()
    categorys = Category.objects.all()
    charts_data = {'time_labels': time_labels}
    for category in categorys:
        new_data_set = get_zeroed_data_set(time_labels)
        charts_data[category.name] = new_data_set
    financial_changes = FinancialChange.objects.all()
    for financial_change in financial_changes:
        index = get_data_set_index(financial_change.date, time_labels)
        if financial_change.direction == 'I':
            charts_data[financial_change.category.name][index] += financial_change.amount_gr
        else:
            charts_data[financial_change.category.name][index] -= financial_change.amount_gr
    add_real_estates_category(charts_data)
    translate_category_names(charts_data)
    return charts_data


def get_financial_change_by_asset_type():
    time_labels = get_time_labels()
    asset_types = AssetType.objects.all()
    chart_data = {'time_labels': time_labels}
    for asset_type in asset_types:
        new_data_set = get_zeroed_data_set(time_labels)
        chart_data[asset_type.name] = new_data_set
    financial_changes = FinancialChange.objects.all()
    for financial_change in financial_changes:
        index = get_data_set_index(financial_change.date, time_labels)
        if financial_change.direction == 'I':
            chart_data[financial_change.asset_type.name][index] += financial_change.amount_gr
        else:
            chart_data[financial_change.asset_type.name][index] -= financial_change.amount_gr
    translate_asset_type_names(chart_data)
    return chart_data


def get_asset_sums():
    asset_types = AssetType.objects.all()
    asset_sum_data = {}
    for asset_type in asset_types:
        asset_sum_data[asset_type.name] = decimal.Decimal(0.00)
    financial_changes = FinancialChange.objects.all()
    for financial_change in financial_changes:
        if financial_change.direction == 'I':
            asset_sum_data[financial_change.asset_type.name] += financial_change.amount_gr
        else:
            asset_sum_data[financial_change.asset_type.name] -= financial_change.amount_gr
    translate_asset_type_names(asset_sum_data)

    new_chart_data = {'labels': ['Nieruchomości', 'Gotówka', 'Akcje', 'Kredyt', 'Pożyczka'],
                      'data': [asset_sum_data['nieruchomosci'], asset_sum_data['pieniadze'],
                               asset_sum_data['akcje'], asset_sum_data['kredyt'], asset_sum_data['pozyczka']],
                      'colours': ["#800000", "#228B22", "#87CEFA", "#9932CC", "#BDB76B"]}
    return new_chart_data


def translate_asset_type_names(chart_asset_type_data):
    chart_asset_type_data['pozyczka'] = chart_asset_type_data.pop('Pożyczka')
    chart_asset_type_data['kredyt'] = chart_asset_type_data.pop('Kredyt')
    chart_asset_type_data['akcje'] = chart_asset_type_data.pop('Akcje')
    chart_asset_type_data['nieruchomosci'] = chart_asset_type_data.pop('Nieruchomość')
    chart_asset_type_data['pieniadze'] = chart_asset_type_data.pop('Pieniądze')
    return chart_asset_type_data


def get_time_labels():
    financial_changes = FinancialChange.objects.all()
    earliest_year = financial_changes[0].date.year
    earliest_month = financial_changes[0].date.month
    latest_year = financial_changes[0].date.year
    latest_month = financial_changes[0].date.month
    for financial_change in financial_changes:
        if financial_change.date.year < earliest_year:
            earliest_year = financial_change.date.year
            earliest_month = financial_change.date.month
        elif financial_change.date.year == earliest_year and financial_change.date.month < earliest_month:
            earliest_month = financial_change.date.month
        if financial_change.date.year > latest_year:
            latest_year = financial_change.date.year
            latest_month = financial_change.date.month
        elif financial_change.date.year == latest_year and financial_change.date.month > latest_month:
            latest_month = financial_change.date.month
    time_labels = []
    for year in range(earliest_year, latest_year + 1):
        for month in range(1, 13):
            if ((year == earliest_year and month >= earliest_month) or
                    (year == latest_year and month <= latest_month) or (
                            year != earliest_year and year != latest_year
                    )):
                new_time_label = f'{months_dict[month]}-{year}'
                time_labels.append(new_time_label)
    return time_labels


def get_zeroed_data_set(time_labels):
    data_set = []
    for label in time_labels:
        data_set.append(decimal.Decimal(0.00))
    return data_set


def get_data_set_index(date, time_labels: list):
    date_label = f'{months_dict[date.month]}-{date.year}'
    date_index = time_labels.index(date_label)
    return date_index


def sum_accumulation(monthly_agregation: list):
    for month_sum in monthly_agregation:
        index = monthly_agregation.index(month_sum)
        if index > 0:
            monthly_agregation[index] += monthly_agregation[index - 1]


def translate_category_names(chart_category_data: dict):
    chart_category_data['pozyczki'] = chart_category_data.pop('Pożyczki')
    chart_category_data['praca'] = chart_category_data.pop('Praca')
    chart_category_data['dom'] = chart_category_data.pop('Dom')
    chart_category_data['podatki'] = chart_category_data.pop('Podatki')
    chart_category_data['firma'] = chart_category_data.pop('Firma')
    chart_category_data['akcje'] = chart_category_data.pop('Akcje')
    chart_category_data['wat'] = chart_category_data.pop('WAT')
    chart_category_data['zycie'] = chart_category_data.pop('Życie')
    chart_category_data['pa8'] = chart_category_data.pop('Przy Agorze 8')
    chart_category_data['pa7'] = chart_category_data.pop('Przy Agorze 7')
    return chart_category_data


def add_real_estates_category(chart_category_data: dict):
    nieruchomosci_data = get_zeroed_data_set(chart_category_data['time_labels'])
    for time_label in chart_category_data['time_labels']:
        index = chart_category_data['time_labels'].index(time_label)
        nieruchomosci_data[index] = chart_category_data['Przy Agorze 8'][index] + chart_category_data['Przy Agorze 7'][index]
    chart_category_data['nieruchomosci'] = nieruchomosci_data
