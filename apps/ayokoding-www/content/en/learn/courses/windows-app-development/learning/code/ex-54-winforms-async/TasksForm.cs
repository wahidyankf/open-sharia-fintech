using System.Windows.Forms;

namespace WinFormsAsyncExample;

public sealed class TasksForm : Form
{
    private readonly Label status = new() { Text = "Idle" };

    public TasksForm()
    {
        Controls.Add(status);
        Shown += async (_, _) => await LoadAsync();
    }

    private async Task LoadAsync()
    {
        status.Text = "Loading";
        await Task.Delay(1);
        status.Text = "Loaded";
    }
}
