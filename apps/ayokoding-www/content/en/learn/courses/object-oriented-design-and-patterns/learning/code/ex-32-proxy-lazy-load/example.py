"""Example 32: A Virtual Proxy Defers an Expensive Load."""


class RealImage:  # => the EXPENSIVE real subject -- loading it costs real work
    load_count: int = 0  # => a class-level counter so the example can OBSERVE loading

    def __init__(self, filename: str) -> None:  # => construction itself IS the expensive step
        self.filename = filename  # => stores filename on this instance
        RealImage.load_count += 1  # => every construction increments the shared counter
        print(f"loading {filename} from disk")  # => simulates the expensive I/O happening

    def render(self) -> str:  # => defines the render() method
        return f"rendering {self.filename}"  # => returns this value to the caller


class ImageProxy:  # => the VIRTUAL PROXY -- stands in for a RealImage not yet loaded
    def __init__(self, filename: str) -> None:  # => cheap -- no loading happens here
        self._filename: str = filename  # => stores only the filename, nothing expensive
        self._real: RealImage | None = None  # => the real subject, created LAZILY

    def render(self) -> str:  # => same interface as RealImage.render() -- callers can't tell
        if self._real is None:  # => only construct the real subject on FIRST access
            self._real = RealImage(self._filename)  # => the expensive load happens HERE
        return self._real.render()  # => delegates to the now-loaded real subject


proxy: ImageProxy = ImageProxy("photo.png")  # => cheap -- RealImage.load_count is still 0
print(RealImage.load_count)  # => confirms NOTHING loaded yet, just constructing the proxy
# => Output: 0
proxy.render()  # => first access -- triggers the actual, expensive load
proxy.render()  # => second access -- reuses the ALREADY-loaded RealImage, no reload
print(RealImage.load_count)  # => loaded exactly once, despite two render() calls
# => Output: 1
# => The proxy defers construction of the expensive real subject until the FIRST access, then caches it
