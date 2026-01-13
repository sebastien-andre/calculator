class CalcError(Exception):
    code = "UNKNOWN"

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.code}: {self.message}"


class CalcSyntaxError(CalcError):
    code = "SYNTAX_ERROR"


class CalcMathError(CalcError):
    code = "MATH_ERROR"
