import logging


class ExceptionHelper:
    @staticmethod
    def raise_exception(description: str, line_number: str, function_name: str):
        # ExceptionHelper.raise_exception(str(e), inspect.currentframe().f_lineno, inspect.currentframe().f_code.co_name)
        error_message = f"Error in {function_name}() at line {line_number} ... \n\t\t\t\t{description}"
        logging.error(error_message)
        raise Exception(error_message)
