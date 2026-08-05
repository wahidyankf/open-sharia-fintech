using WindowsTasks;
using Xunit;

namespace WindowsTasks.Tests;

public sealed class TaskViewModelTests
{
    [Fact]
    public async Task LoadAsync_populates_observable_tasks_and_reports_completion()
    {
        var viewModel = new TaskViewModel(
            new FakeRepository([new TaskItem(1, "Review invoices", false)]),
            new MemorySettingsStore("")
        );

        await viewModel.LoadAsync();

        Assert.Single(viewModel.Tasks);
        Assert.Equal(100, viewModel.Progress);
        Assert.False(viewModel.IsBusy);
        Assert.Equal("", viewModel.ErrorMessage);
    }

    [Fact]
    public async Task LoadAsync_surfaces_cancellation_as_recoverable_state()
    {
        var viewModel = new TaskViewModel(new CancellingRepository(), new MemorySettingsStore(""));

        await viewModel.LoadAsync();

        Assert.Equal("Load cancelled.", viewModel.ErrorMessage);
        Assert.False(viewModel.IsBusy);
    }

    [Fact]
    public async Task LoadAsync_preserves_a_user_entered_filter_and_reloads_it_on_the_next_launch()
    {
        var settings = new MemorySettingsStore("saved filter");
        var viewModel = new TaskViewModel(
            new FakeRepository([new TaskItem(1, "Review invoices", false)]),
            settings
        );
        viewModel.Filter = "invoices";

        await viewModel.LoadAsync();

        Assert.Equal("invoices", settings.Filter);
        Assert.Single(viewModel.Tasks);

        var reloaded = new TaskViewModel(
            new FakeRepository([new TaskItem(1, "Review invoices", false)]),
            settings
        );
        await reloaded.LoadAsync();

        Assert.Equal("invoices", reloaded.Filter);
        Assert.Single(reloaded.Tasks);
    }

    private sealed class FakeRepository(IReadOnlyList<TaskItem> tasks) : ITaskRepository
    {
        public Task<IReadOnlyList<TaskItem>> LoadAsync(
            IProgress<int> progress,
            CancellationToken cancellationToken
        )
        {
            progress.Report(100);
            return Task.FromResult(tasks);
        }
    }

    private sealed class CancellingRepository : ITaskRepository
    {
        public Task<IReadOnlyList<TaskItem>> LoadAsync(
            IProgress<int> progress,
            CancellationToken cancellationToken
        ) => Task.FromCanceled<IReadOnlyList<TaskItem>>(new CancellationToken(true));
    }

    private sealed class MemorySettingsStore(string filter) : ISettingsStore
    {
        public string Filter { get; private set; } = filter;

        public Task<string> ReadFilterAsync(CancellationToken cancellationToken) =>
            Task.FromResult(Filter);

        public Task WriteFilterAsync(string newFilter, CancellationToken cancellationToken)
        {
            Filter = newFilter;
            return Task.CompletedTask;
        }
    }
}
