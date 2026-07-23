"""Example 48: A Mediator Decouples Two Collaborators."""


class ChatRoom:  # => the MEDIATOR -- the ONLY object that knows about every Participant
    def __init__(self) -> None:  # => the constructor
        self._members: dict[str, "Participant"] = {}  # => name -> Participant, held HERE

    def register(self, participant: "Participant") -> None:  # => defines register()
        self._members[participant.name] = participant  # => the mediator learns about them

    def relay(self, sender: str, recipient: str, message: str) -> None:  # => defines relay()
        self._members[recipient].receive(sender, message)  # => the mediator looks up and delivers -- senders never do this themselves


class Participant:  # => a COLLABORATOR -- never holds a reference to another Participant
    def __init__(self, name: str, room: ChatRoom) -> None:  # => the constructor
        self.name = name  # => stores name on this instance
        self._room: ChatRoom = room  # => the ONLY collaborator this class ever references
        self.inbox: list[str] = []  # => messages this participant has received

    def send(self, recipient: str, message: str) -> None:  # => defines the send() method
        self._room.relay(self.name, recipient, message)  # => goes THROUGH the mediator, never directly to the recipient

    def receive(self, sender: str, message: str) -> None:  # => defines the receive() method
        self.inbox.append(f"{sender}: {message}")  # => records the delivered message


room: ChatRoom = ChatRoom()  # => constructs room
alice: Participant = Participant("alice", room)  # => alice holds ONLY a reference to room, never to bob
bob: Participant = Participant("bob", room)  # => bob holds ONLY a reference to room, never to alice
room.register(alice)  # => the mediator learns alice exists
room.register(bob)  # => the mediator learns bob exists

alice.send("bob", "hello")  # => routed THROUGH the mediator, not a direct alice -> bob call
print(bob.inbox)  # => the mediator delivered the message despite alice never touching bob
# => Output: ['alice: hello']
print(hasattr(alice, "bob") or "bob" in vars(alice))  # => alice holds no reference to bob at all
# => Output: False
# => Neither Participant ever references the other directly -- every interaction is routed through ChatRoom
