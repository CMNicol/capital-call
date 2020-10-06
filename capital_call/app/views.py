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


class Create(APIView):
    def post(self, request: HttpRequest):
        form = CallForm(request.POST)
        if form.is_valid():
            call_controller = CallController(
                date=form.cleaned_data['date'].__str__(),
                investment_name=form.cleaned_data['investment_name'],
                capital_required=form.cleaned_data['capital_requirement']
            )
            call_controller.calculate_call(is_confirmed=False)
            request.session['preview'] = call_controller.preview_table_data
            request.session['call'] = {'date': call_controller.date,
                                       'investment_name': call_controller.investment_name,
                                       'capital_required': call_controller.capital_required
                                       }

            return render(request, 'preview_call.html', {'call': request.session['call'], 'preview': request.session['preview']})
        else:
            return render(request, 'call_confirm_invalid.html')

    def get(self, request: HttpRequest):
        form = CallForm()
        return render(request, 'create_call.html', {'form': form})


class Dashboard(APIView):
    def get(self, request: HttpRequest):
        call_fund_amount_list, column_headers = self.__get_dashboard_data()
        return render(request, 'dashboard.html',
                      {'dashboard_data': call_fund_amount_list, 'column_headers': column_headers})

    def __get_dashboard_data(self):
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


class Confirm(APIView):
    def post(self, request: HttpRequest):
        call_controller = CallController(
            date=request.session['call']['date'],
            investment_name=request.session['call']['investment_name'],
            capital_required=request.session['call']['capital_required']
        )
        call_controller.calculate_call(is_confirmed=True)
        return render(request, 'call_confirmed.html')

