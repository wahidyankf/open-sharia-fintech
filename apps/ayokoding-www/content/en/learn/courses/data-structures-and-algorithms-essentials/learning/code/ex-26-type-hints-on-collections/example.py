"""Example 26: Type Hints on Collection Parameters."""


# cart holds quantities per line; prices maps item name -> unit price (co-22).
def total_price(
    cart: list[int], prices: dict[str, int]
) -> int:  # => typed collection params
    names = list(prices.keys())  # => names[i] pairs positionally with cart[i] here
    return sum(qty * prices[name] for qty, name in zip(cart, names))
    # => zip pairs (quantity, item name); the generator sums qty * unit price per pair


cart: list[int] = [2, 1, 3]  # => quantities: 2 apples, 1 bread, 3 milk
prices: dict[str, int] = {"apple": 1, "bread": 3, "milk": 2}  # => unit price per item
grand_total = total_price(cart, prices)  # => 2*1 + 1*3 + 3*2 = 2 + 3 + 6
print(grand_total)  # => Output: 11

assert grand_total == 11  # => confirms the typed function computed the correct total
print("ex-26 OK")  # => Output: ex-26 OK
