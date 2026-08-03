using System.IO;

namespace WindowsTasks;

public partial class MainWindow : System.Windows.Window
{
    public MainWindow()
    {
        InitializeComponent();
        var dataRoot = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "WindowsTasks"
        );
        Directory.CreateDirectory(dataRoot);
        DataContext = new TaskViewModel(
            new SqliteTaskRepository(Path.Combine(dataRoot, "tasks.db")),
            new JsonSettingsStore(Path.Combine(dataRoot, "settings.json"))
        );
    }
}
