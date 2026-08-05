// Example 34: executable .NET behavior probe.
var tasks = new System.Collections.ObjectModel.ObservableCollection<string>();
var added = false;
tasks.CollectionChanged += (_, args) =>
    added = args.Action == System.Collections.Specialized.NotifyCollectionChangedAction.Add;
tasks.Add("Review invoices");
if (!added || tasks.Count != 1)
    throw new InvalidOperationException("ObservableCollection did not publish its add.");
Console.WriteLine("ObservableCollection published a task addition.");
