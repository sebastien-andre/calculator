import pytest
from io import StringIO
from unittest.mock import patch

from calc.cli.main import CommandLoop


@pytest.fixture
def command_loop():
    # Create a fresh CommandLoop for each test
    return CommandLoop()


def test_cli_evaluate_expression(command_loop):
    # Simulate user input
    with patch('builtins.input', return_value='2 + 3'):
        with patch('builtins.print') as mock_print:
            command_loop.handle_command('2 + 3')
            # Should print the result
            mock_print.assert_called_with('= 5')


def test_cli_help_command(command_loop):
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('help')
        # Should print help text
        assert mock_print.called
        call_args = str(mock_print.call_args)
        assert 'Commands' in call_args or 'history' in call_args


def test_cli_history_command(command_loop):
    # Add some history
    command_loop.handle_command('5 + 5')
    command_loop.handle_command('10 * 2')
    
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('history')
        # Should print history
        assert mock_print.called


def test_cli_history_empty(command_loop):
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('history')
        # Should say no history
        mock_print.assert_called_with('No history')


def test_cli_clear_command(command_loop):
    # Add some history
    command_loop.handle_command('1 + 1')
    command_loop.handle_command('2 + 2')
    
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('clear')
        mock_print.assert_called_with('History cleared')
    
    # Verify history is empty
    history = command_loop.session.get_history()
    assert len(history) == 0


def test_cli_reset_command(command_loop):
    # Add some history
    command_loop.handle_command('5 + 5')
    
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('reset')
        mock_print.assert_called_with('Calculator reset')
    
    # Verify history is empty
    history = command_loop.session.get_history()
    assert len(history) == 0


def test_cli_quit_command(command_loop):
    assert command_loop.running == True
    
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('quit')
        mock_print.assert_called_with('Goodbye')
    
    # Should set running to False
    assert command_loop.running == False


def test_cli_invalid_expression(command_loop):
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('2 + + 3')
        # Should print error
        assert 'Error' in str(mock_print.call_args)


def test_cli_division_by_zero(command_loop):
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('10 / 0')
        # Should print error
        assert 'Error' in str(mock_print.call_args)


def test_cli_operator_precedence(command_loop):
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('2 + 3 * 4')
        mock_print.assert_called_with('= 14')


def test_cli_parentheses(command_loop):
    with patch('builtins.print') as mock_print:
        command_loop.handle_command('(2 + 3) * 4')
        mock_print.assert_called_with('= 20')


def test_cli_stores_history(command_loop):
    command_loop.handle_command('5 + 5')
    command_loop.handle_command('10 * 2')
    
    history = command_loop.session.get_history()
    assert len(history) == 2
    assert history[0]["expression"] == "5 + 5"
    assert history[0]["result"] == "10"
    assert history[1]["expression"] == "10 * 2"
    assert history[1]["result"] == "20"
