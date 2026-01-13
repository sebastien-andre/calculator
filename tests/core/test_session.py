from decimal import Decimal

from calc.core.session import CalculatorSession


def test_session_evaluate():
    session = CalculatorSession()
    result = session.evaluate("2 + 3")
    assert result == "5"


def test_session_stores_history():
    session = CalculatorSession()
    session.evaluate("5 + 5")
    session.evaluate("10 * 2")
    
    history = session.get_history()
    assert len(history) == 2
    assert history[0]["expression"] == "5 + 5"
    assert history[0]["result"] == "10"
    assert history[1]["expression"] == "10 * 2"
    assert history[1]["result"] == "20"


def test_session_history_limit():
    session = CalculatorSession()
    
    # add more than 10 entries
    for i in range(15):
        session.evaluate(f"{i} + 1")
    
    history = session.get_history()
    # should only keep last 10
    assert len(history) == 10
    # oldest should be "5 + 1" = 6
    assert history[0]["expression"] == "5 + 1"
    assert history[0]["result"] == "6"


def test_session_clear_history():
    session = CalculatorSession()
    session.evaluate("1 + 1")
    session.evaluate("2 + 2")
    
    session.clear_history()
    history = session.get_history()
    assert len(history) == 0


def test_session_format_result():
    session = CalculatorSession()
    result = session.evaluate("10 / 3")
    # should format to 2 decimal places
    assert result == "3.33"


def test_session_reset():
    session = CalculatorSession()
    session.evaluate("5 + 5")
    
    session.reset()
    history = session.get_history()
    assert len(history) == 0
