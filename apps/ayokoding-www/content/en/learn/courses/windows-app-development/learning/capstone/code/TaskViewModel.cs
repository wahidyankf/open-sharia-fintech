using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

namespace WindowsTasks;

public sealed class TaskViewModel : INotifyPropertyChanged
{
    private readonly ITaskRepository repository;
    private readonly ISettingsStore settings;
    private CancellationTokenSource? loadCancellation;
    private string filter = string.Empty;
    private bool filterWasSetByUser;
    private string errorMessage = string.Empty;
    private int progress;
    private bool isBusy;

    public TaskViewModel(ITaskRepository repository, ISettingsStore settings)
    {
        this.repository = repository;
        this.settings = settings;
        LoadCommand = new AsyncRelayCommand(LoadAsync, () => !IsBusy);
        CancelCommand = new RelayCommand(() => loadCancellation?.Cancel(), () => IsBusy);
    }

    public ObservableCollection<TaskItem> Tasks { get; } = [];
    public ICommand LoadCommand { get; }
    public ICommand CancelCommand { get; }

    public string Filter
    {
        get => filter;
        set => SetFilter(value, wasSetByUser: true);
    }

    public string ErrorMessage
    {
        get => errorMessage;
        private set
        {
            if (errorMessage == value)
                return;
            errorMessage = value;
            OnPropertyChanged();
        }
    }

    public int Progress
    {
        get => progress;
        private set
        {
            if (progress == value)
                return;
            progress = value;
            OnPropertyChanged();
        }
    }

    public bool IsBusy
    {
        get => isBusy;
        private set
        {
            if (isBusy == value)
                return;
            isBusy = value;
            OnPropertyChanged();
            ((AsyncRelayCommand)LoadCommand).RaiseCanExecuteChanged();
            ((RelayCommand)CancelCommand).RaiseCanExecuteChanged();
        }
    }

    public async Task LoadAsync()
    {
        if (IsBusy)
            return;
        IsBusy = true;
        ErrorMessage = string.Empty;
        loadCancellation = new CancellationTokenSource();
        try
        {
            if (!filterWasSetByUser)
            {
                SetFilter(
                    await settings.ReadFilterAsync(loadCancellation.Token),
                    wasSetByUser: false
                );
            }
            var reporter = new Progress<int>(value => Progress = value);
            var loaded = await repository.LoadAsync(reporter, loadCancellation.Token);
            Tasks.Clear();
            foreach (
                var task in loaded.Where(task =>
                    task.Title.Contains(Filter, StringComparison.OrdinalIgnoreCase)
                )
            )
                Tasks.Add(task);
            await settings.WriteFilterAsync(Filter, loadCancellation.Token);
        }
        catch (OperationCanceledException)
        {
            ErrorMessage = "Load cancelled.";
        }
        catch (Exception ex)
        {
            ErrorMessage = $"Could not load tasks: {ex.Message}";
        }
        finally
        {
            loadCancellation.Dispose();
            loadCancellation = null;
            IsBusy = false;
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    private void SetFilter(string value, bool wasSetByUser)
    {
        filterWasSetByUser |= wasSetByUser;
        if (filter == value)
            return;
        filter = value;
        OnPropertyChanged(nameof(Filter));
    }

    private void OnPropertyChanged([CallerMemberName] string? name = null) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
