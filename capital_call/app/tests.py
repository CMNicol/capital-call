from django.test import TestCase
from .models import DataCall, DataFund, DataCommitment, DataFundInvestment
from datetime import date
from .callcontroller import CallController


# Create your tests here.
class TestModels(TestCase):
    test_data_call_record_1 = DataCall(pk=1, date=date(2018, 1, 31), investment_name='Investment 1',
                                       capital_requirement=9500000)
    test_data_call_record_2 = DataCall(pk=2, date=date(2019, 1, 31), investment_name='Investment 2',
                                       capital_requirement=10000000)

    test_dfi_record_1 = DataFundInvestment(
        pk=1,
        call_id=test_data_call_record_1,
        commitment_id=DataCommitment.objects.first(),
        fund_id=DataFund.objects.first(),
        investment_amount=9500000
    )
    test_dfi_record_2 = DataFundInvestment(
        pk=2,
        call_id=test_data_call_record_2,
        commitment_id=DataCommitment.objects.first(),
        fund_id=DataFund.objects.first(),
        investment_amount=500000
    )
    test_dfi_record_3 = DataFundInvestment(
        pk=3,
        call_id=test_data_call_record_2,
        commitment_id=DataCommitment.objects.all()[1],
        fund_id=DataFund.objects.all()[1],
        investment_amount=9500000
    )

    def setUp(cls):
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

    def test_foreign_key_funds_and_commitments(self):
        fundFromDataFund = DataFund.objects.get(fundName='Fund 2')
        fundFromDataCommitment = DataCommitment.objects.get(fund_id=fundFromDataFund)
        self.assertEqual(fundFromDataCommitment, DataCommitment.objects.get(pk=2))

    def test_call_calculation_1(self):
        new_call = CallController(date=date(2018, 1, 31), investment_name='Investment 1', capital_required=9500000)
        new_call.calculate_call()
        self.assertEqual(DataCall.objects.last().investment_name, self.test_data_call_record_1.investment_name)
        self.assertEqual(DataFundInvestment.objects.first().investment_amount, self.test_dfi_record_1.investment_amount)

    def test_call_calculation_2(self):
        new_call = CallController(date=date(2018, 1, 31), investment_name='Investment 1', capital_required=9500000)
        new_call.calculate_call()
        new_call = CallController(date=date(2018, 4, 30), investment_name='Investment 2', capital_required=10000000)
        new_call.calculate_call()

        self.assertEqual(DataFundInvestment.objects.all()[0].call_id, self.test_dfi_record_1.call_id)
        self.assertEqual(DataFundInvestment.objects.all()[0].fund_id, self.test_dfi_record_1.fund_id)
        self.assertEqual(DataFundInvestment.objects.all()[0].commitment_id, self.test_dfi_record_1.commitment_id)
        self.assertEqual(DataFundInvestment.objects.all()[0].investment_amount,
                         self.test_dfi_record_1.investment_amount)
        self.assertEqual(DataFundInvestment.objects.all()[1].call_id, self.test_dfi_record_2.call_id)
        self.assertEqual(DataFundInvestment.objects.all()[1].fund_id, self.test_dfi_record_2.fund_id)
        self.assertEqual(DataFundInvestment.objects.all()[1].commitment_id, self.test_dfi_record_2.commitment_id)
        self.assertEqual(DataFundInvestment.objects.all()[1].investment_amount,
                         self.test_dfi_record_2.investment_amount)
        self.assertEqual(DataFundInvestment.objects.all()[2].call_id, self.test_dfi_record_3.call_id)
        self.assertEqual(DataFundInvestment.objects.all()[2].fund_id, self.test_dfi_record_3.fund_id)
        self.assertEqual(DataFundInvestment.objects.all()[2].commitment_id, self.test_dfi_record_3.commitment_id)
        self.assertEqual(DataFundInvestment.objects.all()[2].investment_amount,
                         self.test_dfi_record_3.investment_amount)
