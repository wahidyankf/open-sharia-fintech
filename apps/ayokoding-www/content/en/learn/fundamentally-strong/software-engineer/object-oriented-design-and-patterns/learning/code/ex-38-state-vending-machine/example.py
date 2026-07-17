"""Example 38: A Vending Machine State Machine, Not Boolean Flags."""

import abc  # => imports the abc module


class VendingMachine:  # => the CONTEXT -- holds whichever state object is CURRENT
    def __init__(self) -> None:  # => the constructor
        self.state: "MachineState" = NoCoinState()  # => starts in the NoCoin state

    def insert_coin(self) -> str:  # => delegates the DECISION to the current state object
        return self.state.insert_coin(self)  # => returns this value to the caller

    def dispense(self) -> str:  # => delegates the DECISION to the current state object
        return self.state.dispense(self)  # => returns this value to the caller


class MachineState(abc.ABC):  # => one state object PER machine state, not a flag/enum
    @abc.abstractmethod
    def insert_coin(self, machine: VendingMachine) -> str:  # => no body -- required
        ...  # => the ellipsis stub -- concrete states below fill this in

    @abc.abstractmethod
    def dispense(self, machine: VendingMachine) -> str:  # => no body -- required
        ...  # => the ellipsis stub -- concrete states below fill this in


class NoCoinState(MachineState):  # => the machine has NO coin inserted yet
    def insert_coin(self, machine: VendingMachine) -> str:  # => the LEGAL transition here
        machine.state = HasCoinState()  # => switches the context to a DIFFERENT state object
        return "coin accepted"  # => returns this value to the caller

    def dispense(self, machine: VendingMachine) -> str:  # => the ILLEGAL transition here
        raise ValueError("insert a coin first")  # => rejected -- no coin, nothing to dispense


class HasCoinState(MachineState):  # => the machine already HAS a coin inserted
    def insert_coin(self, machine: VendingMachine) -> str:  # => the ILLEGAL transition here
        raise ValueError("coin already inserted")  # => rejected -- can't insert a second coin

    def dispense(self, machine: VendingMachine) -> str:  # => the LEGAL transition here
        machine.state = NoCoinState()  # => switches back to the NoCoin state
        return "item dispensed"  # => returns this value to the caller


machine: VendingMachine = VendingMachine()  # => constructs machine
print(machine.insert_coin())  # => legal from NoCoinState
# => Output: coin accepted
print(machine.dispense())  # => legal from HasCoinState -- item is released
# => Output: item dispensed

try:  # => the block below is expected to raise
    machine.dispense()  # => ILLEGAL: back in NoCoinState, nothing to dispense
except ValueError as exc:  # => catches the ValueError raised above
    print(exc)  # => confirms the illegal transition was rejected, not silently ignored
# => Output: insert a coin first
# => Each state is its OWN object that decides which transitions are legal, replacing scattered if/flag checks
