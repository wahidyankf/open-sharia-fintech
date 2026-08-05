var ticket = new Ticket("open");
var closed = ticket with { Status = "closed" };
Console.WriteLine(ticket.Status + ":" + closed.Status); // => Output: open:closed

record Ticket(string Status);
