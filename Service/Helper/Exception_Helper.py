from enum import Enum
import inspect


class Exception_Helper:
    @staticmethod
    def raise_exception(description: str, line_number: str, function_name: str):
        error_message = f"Error in {function_name}() at line {line_number} ... \n\t\t\t\t{description}"
        raise Exception(error_message)
