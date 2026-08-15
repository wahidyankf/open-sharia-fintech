// => Declares the C++17 capstone library interface.
#pragma once
// => Provides the string and vector types in the public signature.
#include <string>
#include <vector>
// => Summarizes a non-empty task list or throws an exception.
std::string summarize(const std::vector<std::string>& tasks);
