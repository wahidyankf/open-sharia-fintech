# Specialized agents receive different capability partitions.
research = ("search", "read")
# The executor receives actions only it needs.
delivery = ("write", "status")
# Neither agent must select from the combined four tools.
assert len(research) == len(delivery) == 2
# The partitions retain every total capability once.
assert set(research + delivery) == {"search", "read", "write", "status"}
# Print the focused agent surfaces.
print(research, delivery)
