"""
QVEX Core Infrastructure Module
Author: Adel Gachkar
Version: 0.1.0
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

__version__ = "0.1.0"
__author__ = "Adel Gachkar"

# Export the core graph and computation components
try:
    from .graph import Graph, ComputationalGraph
    __all__ = ["Graph", "ComputationalGraph"]
except ImportError as e:
    # Fallback when the graph module is imported stand-alone
    try:
        from core.graph import Graph, ComputationalGraph
        __all__ = ["Graph", "ComputationalGraph"]
    except ImportError as inner_e:
        logger.warning(f"Could not load core Graph components: {inner_e}")
        __all__ = []
