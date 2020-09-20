from django.shortcuts import render
from .models import DataFundInvestment, DataFund, DataCall
from .forms import CallForm
from .callcontroller import CallController
from django.shortcuts import redirect, reverse


# Create your views here.
def home(request):
    return render(request, 'homepage.html', {})


def dashboard(request):
    a_list_of_lists, column_headers = get_dashboard_data()
    return render(request, 'dashboard.html', {'dashboard_data': a_list_of_lists, 'column_headers': column_headers})


def create_call(request):
    if request.method == 'POST':
        form = CallForm(request.POST)
        if form.is_valid():
            call_controller = CallController(
                date=form.cleaned_data['date'],
                investment_name=form.cleaned_data['investment_name'],
                capital_required=form.cleaned_data['capital_requirement']
            )
        call_controller.calculate_call_for_preview()
        return render(request, 'create_call.html', {'form': form, 'call': call_controller})

    form = CallForm()
    return render(request, 'create_call.html', {'form': form})


def confirm_call(request):
    if request.method == 'POST':
        form = CallForm(request.POST)
        if form.is_valid():
            call_controller = CallController(
                date=form.cleaned_data['date'],
                investment_name=form.cleaned_data['investment_name'],
                capital_required=form.cleaned_data['capital_requirement']
            )
            call_controller.calculate_call()
            call_controller.confirm()
            return redirect(dashboard)
        else:
            return redirect(error)


def error(request):
    return render(request, 'error.html')


def cancel(request):
    return redirect(create_call)


def get_dashboard_data():
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
    return a_list_of_lists, column_headers
