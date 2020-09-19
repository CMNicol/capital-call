from .models import DataCommitment, DataFundInvestment, DataCall, DataFund
from django.db.models import QuerySet
from datetime import date


class Call:

    def __init__(self, date, investment_name, capital_required: int):
        self.date = date
        self.investment_name = investment_name
        self.capital_required = capital_required


class Controller:

    @staticmethod
    def calc_undrawn_capital(call: Call):

        def add_all(records: QuerySet) -> int:
            total = 0
            for record in records:
                total += record.investment_amount
            return total

        capital_to_find = call.capital_required
        commitments = DataCommitment.objects.all()
        new_dfi_entries = []
        # create new DataCall record
        new_call_record = DataCall(date=call.date, investment_name=call.investment_name, capital_requirement=call.capital_required).save()
        k = DataCall.objects.all().last()
        # for each commitment, calculate how much capital has been drawn
        # then calculate how much undrawn capital commitment there is
        for commitment in commitments:
            # get all records in DataFundInvestment that match the commitment and fund id of commitment
            matched_records = DataFundInvestment.objects.filter(commitment_id=commitment.pk).filter(fund_id=commitment.fund_id)
            # add all investment_amounts of matched_records
            drawn_capital = add_all(matched_records)
            undrawn_capital = commitment.amount - drawn_capital

            if undrawn_capital == 0:
                pass
            elif capital_to_find < undrawn_capital:
                new_dfi_entries.append(
                    DataFundInvestment(
                        call_id=k,
                        commitment_id=commitment,
                        fund_id=commitment.fund_id,
                        investment_amount=capital_to_find
                    )
                )
                break
            else:
                new_dfi_entries.append(
                    DataFundInvestment(
                        call_id=k,
                        commitment_id=commitment,
                        fund_id=commitment.fund_id,
                        investment_amount=undrawn_capital
                    )
                )
                capital_to_find = capital_to_find - undrawn_capital

        for entry in new_dfi_entries:
            entry.save()



