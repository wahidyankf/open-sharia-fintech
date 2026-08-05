using System.Windows.Forms;

namespace WinFormsExample;

public sealed class TasksForm : Form
{
    public TasksForm()
    {
        Text = "Windows Tasks";
        Controls.Add(new Button { Text = "Load", Dock = DockStyle.Top });
    }
}
