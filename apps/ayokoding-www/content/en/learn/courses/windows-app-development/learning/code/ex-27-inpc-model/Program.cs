// Example 27: executable .NET behavior probe.
var model = new TaskModel();
string? changed = null;
model.PropertyChanged += (_, args) => changed = args.PropertyName;
model.Title = "Review invoices";
if (changed != nameof(TaskModel.Title))
    throw new InvalidOperationException("INotifyPropertyChanged did not fire.");
Console.WriteLine($"PropertyChanged fired for {changed}.");

sealed class TaskModel : System.ComponentModel.INotifyPropertyChanged
{
    private string title = string.Empty;
    public event System.ComponentModel.PropertyChangedEventHandler? PropertyChanged;
    public string Title
    {
        get => title;
        set
        {
            if (title == value)
                return;
            title = value;
            PropertyChanged?.Invoke(this, new(nameof(Title)));
        }
    }
}
