import requests
import json
from config import current

class InputException(Exception):
    def __str__(self):
        return 'Неверный формат ввода, корректный формат ввода можно узнать отправив команду /help'
class CurrentException(InputException):
    def __str__(self):
        return 'Нельзя конвертировать валюту саму в себя, посмотреть список доступных для конвертации валют можно отправив команду: /list'
class CurrentExceptionFrom(InputException):
    def __str__(self):
        return 'Конвертация такой валюты невозможна, посмотреть список валют для конвертации можно по команде /list'
class CurrentExceptionTo(InputException):
    def __str__(self):
        return 'Конвертация в такую валюту невозможна, посмотреть список валют для конвертации можно по команде /list'
class CurrentExceptionAmount(InputException):
    def __str__(self):
        return 'Некорректный ввод, введите количество валюты целым, положительным числом'

class Message:
    def __init__(self, message):
        self.message = message
        self.f = ''
        self.to = ''
        self.amount = ''
        self.exception = None
    def test(self):
        message = self.message.lower().split('\n')
        try:
            if len(message) != 3:
                raise InputException
            else:
                self.f = message[0].strip()
                if self.f not in current.keys():
                    raise CurrentExceptionFrom
                self.to = message[1].strip()
                if self.to not in current.keys():
                    raise CurrentExceptionTo
                if self.f == self.to:
                    raise CurrentException
                self.amount = message[2].strip()
                if not self.amount.isdigit():
                    raise CurrentExceptionAmount
        except InputException as e:
            self.exception = e
            return False
        else:
            return True
    @staticmethod
    def get_price(to, f, amount):
        url = f"https://api.apilayer.com/currency_data/convert?to={current[to]}&from={current[f]}&amount={amount}"
        access_key = {"apikey": "bzs8XsBZb3Whs6SMCn6iz7Ele2muUHiB"}
        response = requests.request("GET", url, headers=access_key)
        result = json.loads(response.content)
        return result['result']