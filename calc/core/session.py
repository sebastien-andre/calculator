from collections import deque
from decimal import Decimal

from calc.core.expression import eval_expr


class CalculatorSession:
    # manages calculator state, history, and formatting

    def __init__(self):
        # initialize session
        self.history = deque(maxlen=10)
        self.current_value = Decimal("0")

    def evaluate(self, expr):
        # evaluate expression and record in history
        result = eval_expr(expr)
        self.current_value = result
        formatted_result = self.format_result(result)
        self.history.append({
            "expression": expr,
            "result": formatted_result
        })
        return formatted_result

    def format_result(self, value):
        # format to smallest decimal place that makes sense:
        # 0 if whole number, 1 if one decimal, 2 if more
        float_val = float(value)
        
        # check if whole number
        if float_val == int(float_val):
            return str(int(float_val))
        
        # check if one decimal place is enough
        one_decimal = round(float_val, 1)
        if one_decimal == float_val:
            return f"{float_val:.1f}"
        
        # use two decimal places
        return f"{float_val:.2f}"

    def get_history(self):
        # return list of last 10 evaluations
        return list(self.history)

    def clear_history(self):
        self.history.clear()

    def reset(self):
        self.current_value = Decimal("0")
        self.clear_history()
