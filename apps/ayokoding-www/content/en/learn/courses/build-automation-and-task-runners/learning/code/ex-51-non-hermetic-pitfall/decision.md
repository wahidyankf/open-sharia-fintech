# Hidden host dependency

A local system library version that is not declared by the repository is an input the build cannot
reproduce elsewhere. The source checkout may be identical while the library makes output differ.

Declare the library version and acquisition path, or isolate the action from host libraries.
