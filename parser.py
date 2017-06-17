#!/usr/bin/python

from argparse import ArgumentParser


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