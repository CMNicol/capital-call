from django.shortcuts import render
from .models import DataFundInvestment, DataFund, DataCall
from django.forms.models import model_to_dict


# Create your views here.

def dashboard(request):
    calls = DataCall.objects.all()
    a_list_of_lists = []
    column_headers = ['Date', 'Call ID']
    column_headers += list(DataFund.objects.values_list('fundName', flat=True))
    for call in calls:
        a_list = [call.date, call.pk]
        for fund in DataFund.objects.all():
            a = DataFundInvestment.objects.filter(call_id=call).filter(fund_id=fund).first()
            if a:
                a_list.append(a.investment_amount)
            else:
                a_list.append(0)

        a_list_of_lists.append(a_list)

    return render(request, 'dashboard.html', {'dashboard_data': a_list_of_lists, 'column_headers': column_headers})
