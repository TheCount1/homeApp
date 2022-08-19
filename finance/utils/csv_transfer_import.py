import csv
import decimal
import io
import string
from datetime import datetime

from django.db.models import Q

from finance.models import Transfer, Account


def import_csv_transfers(files):
    transactions_csv = csv_transfers_into_list(files['import_file'])
    insert_transfers_from_csv(transactions_csv)


def csv_transfers_into_list(file):
    data_set = file.read().decode('windows-1250')
    io_string = io.StringIO(data_set)
    data = csv.reader(io_string, delimiter=';')
    transaction_file_list = []
    i = 0
    for row in data:
        transaction_file_list.append([])
        for col in row:
            transaction_file_list[i].append(col)
        i = i + 1
    return transaction_file_list


def insert_transfers_from_csv(csv_transactions: list):
    account = get_transfers_account_by_number_string(csv_transactions[20][0])
    for row_num in range(37, len(csv_transactions)):
        if is_transfer_row(csv_transactions[row_num]):
            insert_transfer_from_csv_row(csv_transactions[row_num], account)


def get_transfers_account_by_number_string(account_number_str: string):
    char_list = list([val for val in account_number_str
                      if val.isalpha() or val.isnumeric()])
    account_number_str = "".join(char_list)
    return Account.objects.get(number=account_number_str)


def insert_transfer_from_csv_row(transfer_row: list, account):
    new_transfer = Transfer()
    new_transfer.direction = extract_direction(transfer_row)
    new_transfer.sender_receiver = transfer_row[4]
    new_transfer.title = transfer_row[3]
    new_transfer.outer_account = transfer_row[5]
    new_transfer.operation_date = cast_date(transfer_row[0])
    new_transfer.posting_date = cast_date(transfer_row[1])
    new_transfer.description = transfer_row[2]
    new_transfer.amount_gr = cast_decimal(transfer_row[6])
    new_transfer.balance = cast_decimal(transfer_row[7])
    new_transfer.inner_account = account
    new_transfer.status = 'T'
    if not is_transfer_already_inserted(new_transfer):
        new_transfer.save()



def is_transfer_already_inserted(transfer: Transfer):
   transfers = Transfer.objects.filter(Q(sender_receiver=transfer.sender_receiver) &
                                        Q(title=transfer.title) &
                                        Q(outer_account=transfer.outer_account) &
                                        Q(operation_date=transfer.operation_date) &
                                        Q(posting_date=transfer.posting_date) &
                                        Q(description=transfer.description) &
                                        Q(amount_gr=transfer.amount_gr) &
                                        Q(direction=transfer.direction) &
                                        Q(balance=transfer.balance)).all()
   if transfers.count() == 0:
       return False
   else:
       return True


def is_transfer_row(transfer_row: list):
    if len(transfer_row) == 9:
        if is_date(transfer_row[0]) and is_date(transfer_row[1]) and (len(transfer_row[6]) > 0):
            return True
        else:
            return False
    else:
        return False


def is_date(date_string: string):
    if len(date_string) == 10:
        if date_string[4] == '-' and date_string[7] == '-':
            return True
        else:
            return False
    else:
        return False


def extract_direction(transfer_row: list):
    if transfer_row[6][0] == '-':
        return 'O'
    else:
        return 'I'


def cast_date(date_string: string):
    temp_date = datetime.strptime(date_string, "%Y-%m-%d").date()
    return temp_date


def cast_decimal(decimal_string: string):
    decimal_string = decimal_string.replace(' ', '')
    decimal_string = decimal_string.replace('-', '')
    decimal_string = decimal_string.replace(',', '.')
    return decimal.Decimal(decimal_string)
