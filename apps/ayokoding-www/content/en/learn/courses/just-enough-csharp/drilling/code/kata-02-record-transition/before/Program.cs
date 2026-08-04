var ticket = new Ticket { Status = "open" };
ticket.Status = "closed"; // => mutates shared state
Console.WriteLine(ticket.Status);

record Ticket
{
    public string Status { get; set; } = "";
}
