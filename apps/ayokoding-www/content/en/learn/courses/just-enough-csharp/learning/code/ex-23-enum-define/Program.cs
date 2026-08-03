var state = Status.Ready; // => named state
var message = state switch
{
    Status.Ready => "start",
    Status.Loading => "wait",
    Status.Failed => "retry",
    _ => "retry",
};
Console.WriteLine(message); // => Output: start

enum Status
{
    Loading,
    Ready,
    Failed,
}
