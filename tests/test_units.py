"""Uji konversi satuan milimeter -> inci (satuan internal SketchUp)."""
import importlib.util
import pathlib
import sys
import types

import pytest


def _load_server():
    # Stub modul mcp agar test tidak bergantung pada paket MCP terpasang.
    if "mcp.server.fastmcp" not in sys.modules:
        fastmcp = types.ModuleType("mcp.server.fastmcp")

        class _FastMCP:
            def __init__(self, *a, **k):
                pass

            def tool(self, *a, **k):
                return lambda f: f

            def resource(self, *a, **k):
                return lambda f: f

            def prompt(self, *a, **k):
                return lambda f: f

        fastmcp.FastMCP = _FastMCP
        fastmcp.Context = object
        fastmcp.Image = object
        sys.modules["mcp"] = types.ModuleType("mcp")
        sys.modules["mcp.server"] = types.ModuleType("mcp.server")
        sys.modules["mcp.server.fastmcp"] = fastmcp
    path = pathlib.Path(__file__).resolve().parents[1] / "src" / "sketchup_mcp" / "server.py"
    spec = importlib.util.spec_from_file_location("sketchup_server_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


server = _load_server()


def test_scalar():
    assert server.mm_to_inch(25.4) == pytest.approx(1.0)
    assert server.mm_to_inch(1000) == pytest.approx(39.3700787)


def test_list():
    assert server.mm_to_inch([0, 254, 2540]) == pytest.approx([0.0, 10.0, 100.0])


def test_none():
    assert server.mm_to_inch(None) is None
