# Measured comparison

The capstone's `run.ts` makes two counter updates observable. The virtual-DOM route produces two
complete virtual trees and then reuses unchanged keyed task nodes during patching. The signals route
runs the counter effect twice (initial run plus update) while the independent task-list effect runs
once, proving that the update does not walk unrelated subscribers.

This is not a universal benchmark: real framework scheduling, component shapes, and browser DOM work
matter. It is a concrete measurement of the two minimal mechanisms in this course.
