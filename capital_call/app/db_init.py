from .models import DataCommitment, DataFund
from datetime import date


def db_init():

    DataFund(fundName='Fund 1').save()
    DataFund(fundName='Fund 2').save()
    DataFund(fundName='Fund 3').save()
    DataFund(fundName='Fund 4').save()
    DataFund(fundName='Fund 5').save()

    DataCommitment(fund_id=DataFund.objects.get(fundName='Fund 1'), date=date(2017, 12, 31), amount=10000000).save()
    DataCommitment(fund_id=DataFund.objects.get(fundName='Fund 2'), date=date(2018, 3, 31), amount=15000000).save()
    DataCommitment(fund_id=DataFund.objects.get(fundName='Fund 3'), date=date(2018, 6, 30), amount=10000000).save()
    DataCommitment(fund_id=DataFund.objects.get(fundName='Fund 4'), date=date(2018, 9, 30), amount=15000000).save()
    DataCommitment(fund_id=DataFund.objects.get(fundName='Fund 1'), date=date(2018, 12, 31), amount=10000000).save()
