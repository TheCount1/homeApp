from finance.models import Transfer


class LatestTransformPresentationStringProvider:
    def __init__(self):
        transfer = Transfer.objects.filter(status='T').latest('posting_date')
        self.__set_direction_string(transfer)
        self.__set_from_string(transfer)
        self.__set_to_string(transfer)
        self.__set_directed_amount(transfer)
        self.transfer = transfer

    def __set_direction_string(self, transfer: Transfer):
        if transfer.direction == 'I':
            self.direction = 'przychodzący'
            self.direction_colour = 'green'
        else:
            self.direction = 'wychodzący'
            self.direction_colour = 'red'

    def __set_from_string(self, transfer: Transfer):
        if transfer.direction == 'I':
            self.from_s = transfer.sender_receiver
        else:
            self.from_s = transfer.inner_account.name

    def __set_to_string(self, transfer: Transfer):
        if transfer.direction == 'I':
            self.to = transfer.inner_account.name
        else:
            self.to = transfer.sender_receiver

    def __set_directed_amount(self, transfer: Transfer):
        if transfer.direction == 'I':
            self.directed_amount = '-' + transfer.amount_gr.__str__()
        else:
            self.directed_amount = transfer.amount_gr.__str__()
