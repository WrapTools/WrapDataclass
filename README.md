# WrapDataclass

**WrapDataclass** is a lightweight, modular Python library for working with dataclasses that supports:

- ✅ Nested serialization and deserialization
- ✅ Optional field skipping
- ✅ Dict-like access to attributes
- ✅ JSON read/write with metadata headers
- ✅ Minimal dependencies (only Python standard library)

This is part of the [WrapTools](https://github.com/WrapTools) ecosystem of composable utilities, designed to be imported individually and only when needed.

---

## 🧩 Key Features

| Feature              | Description                                       |
|----------------------|---------------------------------------------------|
| `DictMixin`          | Convert dataclasses to/from dictionaries          |
| `FileMixin`          | Save/load with header metadata (app/version/etc.) |
| `DictLikeMixin`      | Use dataclasses like dictionaries                 |
| `BaseModel`          | Combined mixins for common use                    |
| `from_json_with_header()` | Load data and access saved metadata           |

---

## 🚀 Installation

```bash
# Coming soon via PyPI
pip install wrapdataclass

# Or clone directly
git clone https://github.com/WrapTools/WrapDataclass

