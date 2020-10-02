from .models import DataFundInvestment, DataFund, DataCall
from .forms import CallForm
from .callcontroller import CallController
from django.shortcuts import redirect, reverse, render
from rest_framework.views import APIView
from django.http import HttpRequest, HttpResponse


def home(request):
    return render(request, 'homepage.html', {})


def error(request):
    return render(request, 'error.html')


def get_dashboard_data():
    calls = DataCall.objects.all()
    call_fund_amount_list = []
    column_headers = ['Date', 'Call ID']
    column_headers += list(DataFund.objects.values_list('fundName', flat=True))
    for call in calls:
        call_fund_amount = [call.date, call.pk]
        for fund in DataFund.objects.all():
            dfi = DataFundInvestment.objects.filter(call_id=call).filter(fund_id=fund).first()
            if dfi:
                call_fund_amount.append(dfi.investment_amount)
            else:
                call_fund_amount.append(0)

        call_fund_amount_list.append(call_fund_amount)
    return call_fund_amount_list, column_headers


class Create(APIView):
    def post(self, request: HttpRequest):
        form = CallForm(request.POST)
        if form.is_valid():
            call_controller = CallController(
                date=form.cleaned_data['date'],
                investment_name=form.cleaned_data['investment_name'],
                capital_required=form.cleaned_data['capital_requirement']
            )
            call_controller.calculate_call(is_confirmed=False)
            return render(request, 'create_call.html', {'form': form, 'call': call_controller})
        else:
            return render(request, 'call_confirm_invalid.html')

    def get(self, request: HttpRequest):
        return self.__render_empty_form(request=request)

    def __render_empty_form(self, request: HttpRequest) -> HttpResponse:
        form = CallForm()
        return render(request, 'create_call.html', {'form': form})


class Dashboard(APIView):
    def get(self, request: HttpRequest):
        call_fund_amount_list, column_headers = get_dashboard_data()
        return render(request, 'dashboard.html',
                      {'dashboard_data': call_fund_amount_list, 'column_headers': column_headers})


class Confirm(APIView):
    def post(self, request: HttpRequest):
        form = CallForm(request.POST)
        if form.is_valid():
            call_controller = CallController(
                date=form.cleaned_data['date'],
                investment_name=form.cleaned_data['investment_name'],
                capital_required=form.cleaned_data['capital_requirement']
            )
            call_controller.calculate_call(is_confirmed=True)
            return render(request, 'call_confirmed.html')
        else:
            return render(request, 'call_confirm_invalid.html')

