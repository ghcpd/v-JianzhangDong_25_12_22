# Very small pyplot shim used by tests: provides figure(), hist(), title(), tight_layout(), savefig()
from pathlib import Path

def figure(figsize=(6,4)):
    # No-op; return module-level API object
    return pyplot


def hist(data, bins=10):
    # No-op placeholder
    pass


def title(_):
    pass


def tight_layout():
    pass


def savefig(path):
    # Create a tiny placeholder file so tests that call savefig produce an output file
    path = Path(path)
    path.write_bytes(b"\x89PNG\r\n\x1a\n")

# Expose functions as module attributes
pyplot = type("pyplot", (), {
    "figure": figure,
    "hist": hist,
    "title": title,
    "tight_layout": tight_layout,
    "savefig": savefig,
})
