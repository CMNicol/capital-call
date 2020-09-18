from django.db import models
from django.core.validators import MinValueValidator


class DataFund(models.Model):
    fund_id = models.IntegerField(primary_key=True)
    fundName = models.TextField(max_length=30)


class DataCommitment(models.Model):
    commitment_id = models.IntegerField(primary_key=True)
    fund_id = models.ForeignKey(DataFund, on_delete=models.DO_NOTHING)  # a commitment can only have one fund associated therefore use foreign key
    date = models.DateField()
    amount = models.IntegerField(validators=[MinValueValidator(0)])


class DataCall(models.Model):
    call_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    investment_name = models.TextField(max_length=30)
    capital_requirement = models.IntegerField(validators=[MinValueValidator(0)])


class DataFundInvestment(models.Model):
    dfi_id = models.IntegerField(primary_key=True)
    call_id = models.ForeignKey(DataCall, on_delete=models.DO_NOTHING)
    commitment_id = models.ForeignKey(DataCommitment, on_delete=models.DO_NOTHING)
    fund_id = models.ForeignKey(DataFund, on_delete=models.DO_NOTHING)
    investment_amount = models.IntegerField()
