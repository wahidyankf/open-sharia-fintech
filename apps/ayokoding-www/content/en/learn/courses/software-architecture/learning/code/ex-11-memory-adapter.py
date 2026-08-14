"""Worked Example 11: implement the storage port with local memory."""


class MemoryOrderStore:
    def __init__(self) -> None:
        self.ids: list[str] = []

    def save(self, order_id: str) -> None:
        self.ids.append(order_id)


store = MemoryOrderStore()
store.save("order-1")
print(store.ids)
