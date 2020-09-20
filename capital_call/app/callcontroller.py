from .models import DataCommitment, DataFundInvestment, DataCall, DataFund
from django.db.models import QuerySet
from datetime import date


class CallController:

    def __init__(self, date: date, investment_name: str, capital_required: int):
        self.date = date  # date of call
        self.investment_name = investment_name
        self.capital_required = capital_required  # capital required by the call
        self.new_dfi_entries = []  # DataFundInvestment entries based on the call
        self.preview_table_data = []  # list used to populate the call preview table

    # add_all()
    # This method calculates the sum of the 'investment_amount' fields of all records
    # in records.

    def add_all(self, records: QuerySet) -> int:
        total = 0
        for record in records:
            total += record.investment_amount
        return total

    # calculate_call()
    # This method calculates the capital to be drawn from which commitments and funds.
    # It is configurable to either add new records to the database or calculate a proposed call
    # through the is_confirmed argument.

    def calculate_call(self, is_confirmed: bool):
        capital_to_find = self.capital_required
        commitments = DataCommitment.objects.all()
        # create new DataCall record
        call = DataCall(date=self.date, investment_name=self.investment_name, capital_requirement=self.capital_required)
        if is_confirmed:
            call.save()
            call = DataCall.objects.all().last()
        # for each commitment, calculate how much capital has been drawn
        # then calculate how much undrawn capital commitment there is
        for commitment in commitments:
            # get all records in DataFundInvestment that match the commitment and fund id of commitment
            matched_records = DataFundInvestment.objects.filter(commitment_id=commitment.pk).filter(
                fund_id=commitment.fund_id)
            # add all investment_amounts of matched_records
            drawn_capital = self.add_all(matched_records)
            undrawn_capital = commitment.amount - drawn_capital

            if undrawn_capital == 0:
                pass
            elif capital_to_find < undrawn_capital:
                # the undrawn capital commitment in this commitment will fulfil the remaining capital required
                if is_confirmed:
                    self.new_dfi_entries.append(
                        DataFundInvestment(
                            call_id=call,
                            commitment_id=commitment,
                            fund_id=commitment.fund_id,
                            investment_amount=capital_to_find
                        )
                    )
                else:
                    undrawn_after_drawdown = undrawn_capital - capital_to_find
                    self.preview_table_data.append(
                        self.preview_table_data_entry(
                            commitment=commitment,
                            undrawn_before_drawdown=undrawn_capital,
                            drawdown_notice=capital_to_find,
                            undrawn_after_drawdown=undrawn_after_drawdown
                        )
                    )
                break
            else:
                # the undrawn capital commitment in this commitment will be drawn entirely
                capital_to_find = capital_to_find - undrawn_capital
                if is_confirmed:
                    self.new_dfi_entries.append(
                        DataFundInvestment(
                            call_id=call,
                            commitment_id=commitment,
                            fund_id=commitment.fund_id,
                            investment_amount=undrawn_capital
                        )
                    )
                else:
                    undrawn_after_drawdown = 0
                    self.preview_table_data.append(
                        self.preview_table_data_entry(
                            commitment=commitment,
                            undrawn_before_drawdown=undrawn_capital,
                            drawdown_notice=undrawn_capital,
                            undrawn_after_drawdown=undrawn_after_drawdown
                        )
                    )
        if is_confirmed:
            for entry in self.new_dfi_entries:
                entry.save()

    # preview_table_data_entry()
    # This method returns a dictionary of its arguments.
    # The dictionary represents a single row of the call preview table

    def preview_table_data_entry(self, commitment: DataCommitment, undrawn_before_drawdown: int, drawdown_notice: int,
                                 undrawn_after_drawdown: int) -> dict:
        return {
            'commitment_id': commitment.pk,
            'fund_id': commitment.fund_id.pk,
            'date': commitment.date,
            'fund_name': commitment.fund_id.fundName,
            'committed_amounts': commitment.amount,
            'undrawn_before_drawdown': undrawn_before_drawdown,
            'drawdown': drawdown_notice,
            'undrawn_after_drawdown': undrawn_after_drawdown
        }
