import requests
import xml.etree.ElementTree as ET


class ConvertException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(cur1, cur2, amount):

        if cur1 == cur2:
            raise ConvertException(f'Невозможно перевести одинаковые валюты {base}!')

        if (cur1 == "RUB"):
            cur1_weght = 1
        else:
            etree = ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text)
            val = etree.find('./Valute[CharCode="' + cur1 + '"]/Value')
            if val == None:
                raise ConvertException(f"Валюта {cur1} не найдена!")
            cur1_weght = float(val.text.replace(',', '.'))

        if (cur2 == "RUB"):
            cur2_weght = 1
        else:
            etree = ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text)
            val = etree.find('./Valute[CharCode="' + cur2 + '"]/Value')
            if val == None:
                raise ConvertException(f"Валюта {cur2} не найдена!")
            cur2_weght = float(val.text.replace(',', '.'))

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}!')

        try:
            result = (cur1_weght/cur2_weght)*amount
        except ArithmeticError:
            raise ConvertException(f'Не удалось вычислить !')

        message = f"Цена {amount} {cur1} в {cur2} : {result}"
        return message

    @staticmethod
    def get_all_valutes():
        text = 'RUB\n'
        for i in ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text).findall(
                './Valute/CharCode'):
            text += i.text + "\n"
        return text

    @staticmethod
    def get_rate(char_code_currency="USD"):
        if (char_code_currency=="RUB"): return 1
        return float(ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text).find('./Valute[CharCode="'+char_code_currency+'"]/Value').text.replace(',', '.'))


