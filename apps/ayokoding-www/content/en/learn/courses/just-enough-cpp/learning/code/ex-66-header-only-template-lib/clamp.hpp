// => Avoids multiple inclusion of this header-only template.
#pragma once
// => Defines the full template in the header so callers can instantiate it.
template <typename T>
T clamp(T value, T low, T high) {
  // => Returns low when value is below the allowed range.
  if (value < low) return low;
  // => Returns high when value is above the allowed range.
  if (value > high) return high;
  // => Preserves an already valid value.
  return value;
}
