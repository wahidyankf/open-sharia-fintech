// Example 35: executable .NET behavior probe.
var tasks = new System.Collections.ObjectModel.ObservableCollection<string> { "Review invoices" };
var actions = new List<System.Collections.Specialized.NotifyCollectionChangedAction>();
tasks.CollectionChanged += (_, args) => actions.Add(args.Action);
tasks.Add("Send summary");
tasks.Remove("Review invoices");
if (
    !actions.SequenceEqual([
        System.Collections.Specialized.NotifyCollectionChangedAction.Add,
        System.Collections.Specialized.NotifyCollectionChangedAction.Remove,
    ])
)
    throw new InvalidOperationException("ObservableCollection did not publish both mutations.");
Console.WriteLine("ObservableCollection published add and remove mutations.");
