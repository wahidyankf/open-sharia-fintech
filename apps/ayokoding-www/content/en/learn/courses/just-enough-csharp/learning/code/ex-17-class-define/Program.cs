var card = new Card { Title = "Inbox" }; // => class instance
Console.WriteLine(card.Title); // => Output: Inbox

class Card
{
    public string Title { get; set; } = "";
}
