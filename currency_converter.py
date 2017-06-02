#!/usr/bin/python

from argparse import ArgumentParser
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
from forex_python.converter import RatesNotAvailableError
from json import dump


class InputValues:
    """
    This class represents values from input.
    :param amount - given amount (float)
    :param input_currency - given input currency (string)
    :param output_currency - given output currency (string)
    """
    def __init__(self, amount, input_currency, output_currency):
        self.amount = amount
        self.input_currency = input_currency
        self.output_currency = output_currency


class Parser:
    def try_parse(self):
        """
        This function tries to parse given parameters.
        :raise: ValueError exception if input parameters are invalid
        :return: values (instance of Values) if given parameters are valid, None otherwise
        """
        parser = ArgumentParser()
        parser.add_argument("--amount", type=float)
        parser.add_argument("--input_currency", type=str)
        parser.add_argument("--output_currency", type=str)
        args = parser.parse_args()

        if args.amount is None:
            raise ValueError("Error: --amount parameter is missing.")

        if args.input_currency is None:
            raise ValueError("Error: --input_currency parameter is missing.")

        if args.output_currency is not None:
            return InputValues(args.amount, args.input_currency, args.output_currency)

        return InputValues(args.amount, args.input_currency, None)


class CurrencySymbols:
    def get_symbols_dictionary(self):
        """
        This function returns dictionary of currency symbols.
        :return: dictionary of symbols
        """
        dictionary = dict()
        codes = CurrencyCodes()
        dictionary[codes.get_symbol('USD')] = 'USD'
        for value in CurrencyRates().get_rates('USD'):
            dictionary[codes.get_symbol(value)] = value
        return dictionary


class CurrencyConverter:
    """
    This class represent currency converter which takes values and convert them to data for JSON exporter.
    :param symbols_dictionary - dictionary of currency symbols
    :param values - values from input
    """
    def __init__(self, values, symbols_dictionary):
        self.__symbols_dictionary = symbols_dictionary
        self.__values = values

    def convert(self):
        """
        This function convert values to data for JSON exporter.
        :raise: RatesNotAvailableError if given currency code does not exist
        :return: data to export
        """
        input_currency = self.__set_input_currency()

        converter = CurrencyRates()
        data = dict()
        data['input'] = {}
        data['input']['amount'] = self.__values.amount
        data['input']['currency'] = input_currency
        data['output'] = {}

        if self.__values.output_currency is not None:
            output_currency = self.__set_output_currency()
            result = converter.convert(input_currency, output_currency, self.__values.amount)  # raise exception
            data['output'][output_currency] = round(result, 2)
        else:
            for currency in converter.get_rates(input_currency):
                result = converter.convert(input_currency, currency, self.__values.amount)  # raise exception
                data['output'][currency] = round(result, 2)
        return data

    def __set_input_currency(self):
        """
        This 'private' method sets input currency code.
        If there is match between input_currency and some symbol form dictionary
        then function sets the symbol as an input_currency.
        :return: code of given input currency
        """
        input_currency = self.__symbols_dictionary.get(self.__values.input_currency)
        if input_currency is None:
            input_currency = self.__values.input_currency
        return input_currency

    def __set_output_currency(self):
        """
        This 'private' method sets output currency code (same as self.__set_input_currency())
        :return: code of given output currency
        """
        output_currency = self.__symbols_dictionary.get(self.__values.output_currency)
        if output_currency is None:
            output_currency = self.__values.output_currency
        return output_currency


class JSONExporter:
    """
    This class represents JSON exporter.
    :param path: path to new JSON file
    :param data: data to export
    """
    def __init__(self, path, data):
        self.__path = path
        self.__data = data

    def export(self):
        """
        Function which export data to JSON file with given path.
        """
        with open(self.__path, 'w') as outfile:
            dump(self.__data, outfile, sort_keys=True, indent=4)


class Program:
    def main(self):
        """
        This is the entry point of the program.
        The main function parses input using Parser class, converts values and exports it to JSON file.
        """
        try:
            values = Parser().try_parse()  # parse input into values
            symbols_dictionary = CurrencySymbols().get_symbols_dictionary()  # create currency symbols dictionary
            data = CurrencyConverter(values, symbols_dictionary).convert()  # convert currencies
            JSONExporter('data.json', data).export()  # export data
        except RatesNotAvailableError as exception:
            print(exception)
        except ValueError as exception:
            print(exception)


if __name__ == '__main__':
    Program().main()
