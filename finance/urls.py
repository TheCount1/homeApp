from django.urls import path
from . import views

app_name = 'finance'


urlpatterns = [
    path('', views.home_view, name='home'),
    path('create_financial_change', views.FinancialChangeCreateView.as_view(), name='create_financial_change'),
    path('detail_financial_change/<int:pk>', views.FinancialChangeDetailView.as_view(), name='detail_financial_change'),
    path('list_financial_change', views.FinancialChangeListView.as_view(), name='list_financial_change'),
    path('delete_financial_change/<int:pk>', views.FinancialChangeDeleteView.as_view(), name='delete_financial_change'),
    path('update_financial_change/<int:pk>', views.FinancialChangeUpdateView.as_view(), name='update_financial_change'),
    path('summary_chart_data', views.summary_chart_data, name='summary_chart_data'),
    path('income_expenses_chart_data', views.income_expenses_chart_data, name='income_expenses_chart_data'),
    path('financial_change_monthly_sum_by_category', views.financial_change_monthly_sum_by_category,
         name='financial_change_monthly_sum_by_category'),
    path('financial_change_monthly_sum_by_asset_type', views.financial_change_monthly_sum_by_asset_type,
         name='financial_change_monthly_sum_by_asset_type'),
    path('sum_by_asset_type', views.sum_by_asset_type, name='sum_by_asset_type'),
    path('import_transfer_file', views.import_transfer_file_form, name='import_transfer_file'),
    path('financial_change_from_transfer_create', views.create_financial_change_from_transfer_form,
         name='financial_change_from_transfer')

]