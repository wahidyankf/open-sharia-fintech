// Example 31: executable .NET behavior probe.
var executed = false;
System.Windows.Input.ICommand command = new RelayCommand(() => executed = true, () => true);
command.Execute(null);
if (!executed)
    throw new InvalidOperationException("ICommand.Execute did not invoke the command.");
Console.WriteLine("RelayCommand executed through ICommand.");

sealed class RelayCommand(Action execute, Func<bool> canExecute) : System.Windows.Input.ICommand
{
    public event EventHandler? CanExecuteChanged
    {
        add { }
        remove { }
    }

    public bool CanExecute(object? parameter) => canExecute();

    public void Execute(object? parameter) => execute();
}
