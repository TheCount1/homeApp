import csv
import io

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import FinancialChangeForm, ImportTransfersForm
from finance.models import FinancialChange
# Create your views here.
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from finance.utils.financial_dashboard import get_wealth_sum, get_current_cash
from django import forms
from finance.utils.csv_transfer_import import import_csv_transfers
from finance.utils.financial_change_from_transfer.LatestTransformPresentationStringProvider import LatestTransformPresentationStringProvider

from .utils.charts import get_summary_chart_data, get_income_expenses_chart_data, \
    get_financial_change_monthly_sum_by_category, get_financial_change_by_asset_type, get_asset_sums
from .utils.financial_change_from_transfer.FinancialChangeFromTransferCreator import FinancialChangeFromTransferCreator

def home_view(request):
    context = {
        'wealth_sum': get_wealth_sum('Adrian'),
        'cash_sum': get_current_cash()
    }
    return render(request, 'finance/index.html', context=context)


class FinancialChangeCreateView(CreateView):
    model = FinancialChange
    fields = "__all__"
    success_url = reverse_lazy('finance:list_financial_change')
    widgets = {
        'date': forms.SelectDateWidget()
    }


def import_transfer_file_form(request):
    if request.method == 'POST':
        form = ImportTransfersForm(request.POST, request.FILES)
        if form.is_valid():
            import_csv_transfers(request.FILES)
            return redirect(reverse('finance:financial_change_from_transfer'))
    else:
        form = ImportTransfersForm()
    return render(request, 'finance/import_transfer_file.html', context={'form': form})


def create_financial_change_from_transfer_form(request):
    if request.method == 'POST':
        form = FinancialChangeForm(request.POST)
        if form.is_valid():
            fc_creator = FinancialChangeFromTransferCreator(request.POST)
            fc_creator.set_transfer_status()
            if(request.POST['status'] == 'I'):
                fc_creator.insert_new_financial_change()
            return redirect(reverse('finance:financial_change_from_transfer'))
    else:
        form = FinancialChangeForm()
        transfer_pres = LatestTransformPresentationStringProvider()
    return render(request, 'finance/financial_change_from_transfer_create.html', context={'form': form, 'transfer': transfer_pres})


class FinancialChangeListView(ListView):
    model = FinancialChange
    # Peform any .filter() you want here to only list certain items
    # queryset = Teacher.objects.order_by('first_name')
    # customize the name of the object_list sent to template
    context_object_name = 'object_list'


class FinancialChangeUpdateView(UpdateView):
    model = FinancialChange
    fields = '__all__'
    success_url = reverse_lazy('finance:list_financial_change')


class FinancialChangeDeleteView(DeleteView):
    model = FinancialChange
    success_url = reverse_lazy('finance:list_financial_change')


class FinancialChangeDetailView(DetailView):
    model = FinancialChange


def summary_chart_data(request):
    return JsonResponse(get_summary_chart_data())


def income_expenses_chart_data(request):
    return JsonResponse(get_income_expenses_chart_data())


def financial_change_monthly_sum_by_category(request):
    return JsonResponse(get_financial_change_monthly_sum_by_category())


def financial_change_monthly_sum_by_asset_type(request):
    return JsonResponse(get_financial_change_by_asset_type())


def sum_by_asset_type(request):
    return JsonResponse(get_asset_sums())