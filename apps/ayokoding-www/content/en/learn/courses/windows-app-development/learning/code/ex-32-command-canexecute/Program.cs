// Example 32: executable .NET behavior probe.
var enabled = false;
System.Windows.Input.ICommand command = new RelayCommand(() => { }, () => enabled);
if (command.CanExecute(null))
    throw new InvalidOperationException("Command should start disabled.");
enabled = true;
if (!command.CanExecute(null))
    throw new InvalidOperationException("Command did not reflect its CanExecute predicate.");
Console.WriteLine("ICommand.CanExecute gated the action.");

sealed class RelayCommand(Action execute, Func<bool> canExecute) : System.Windows.Input.ICommand
{
    public event EventHandler? CanExecuteChanged
    {
        add { }
        remove { }
    }

    public bool CanExecute(object? parameter) => canExecute();

    public void Execute(object? parameter)
    {
        if (CanExecute(parameter))
            execute();
    }
}
