# patch_typingio.py
import sys, types
if "typing" in sys.modules:
    import typing
else:
    import typing
if not hasattr(typing, "io"):
    typing.io = types.SimpleNamespace(BinaryIO=bytes, TextIO=str)
if not hasattr(typing, "re"):
    typing.re = types.SimpleNamespace(Pattern=str, Match=str)
