"""Base utilities for tools"""
import json
from typing import Any, Dict, Optional


def build_params(args: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function for building params"""
    params = {}
    if "page_size" in args:
        params["page_size"] = args["page_size"]
    if "include" in args:
        params["include"] = args["include"]
    if "expand" in args:
        params["expand"] = args["expand"]
    return params

