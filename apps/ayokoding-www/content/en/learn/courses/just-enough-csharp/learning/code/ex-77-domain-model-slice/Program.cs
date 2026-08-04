INotifier notifier = new ConsoleNotifier(); // => interface seam
notifier.Send(new Notice("Saved")); // => Output: Saved

record Notice(string Text);

interface INotifier
{
    void Send(Notice n);
}

class ConsoleNotifier : INotifier
{
    public void Send(Notice n) => Console.WriteLine(n.Text);
}
