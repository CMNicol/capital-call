from django.contrib import admin

# Register your models here.
from .models import DataFund, DataCommitment, DataCall, DataFundInvestment
admin.site.register([DataFund, DataCommitment, DataCall, DataFundInvestment])
