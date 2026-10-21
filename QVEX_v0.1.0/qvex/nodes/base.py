import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Node(ABC):
    """
    Abstract base class for all QVEX nodes, augmented with Substrate Context
    to support homogeneous background density, topological phase constraints,
    and global charge/mass conservation invariants.
    """
    def __init__(self, name: Optional[str] = None, node_id: Optional[str] = None, **config: Any):
        self.name = name or node_id or self.__class__.__name__
        self.node_id = node_id or self.name
        self.config = config

    @abstractmethod
    def compute(self, inputs: Dict[str, Any], *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Perform computation given port inputs.
        Can optionally accept substrate_ctx if implemented by the node.
        """
        pass

    def execute(self, inputs: Dict[str, Any], substrate_ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execution wrapper inspecting compute signature to maintain backward compatibility
        with legacy nodes while supplying substrate_ctx to upgraded nodes.
        """
        try:
            sig = inspect.signature(self.compute)
            # Accept substrate_ctx if explicitly declared or if **kwargs is present
            has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
            if "substrate_ctx" in sig.parameters or has_var_kw:
                return self.compute(inputs, substrate_ctx=substrate_ctx)
        except Exception:
            pass
        return self.compute(inputs)


BaseNode = Node


class PassthroughNode(Node):
    """Passes inputs directly to outputs."""
    def compute(self, inputs: Dict[str, Any], *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return dict(inputs)


class PlaceholderNode(Node):
    """Returns an empty dictionary for placeholder or stub nodes."""
    def compute(self, inputs: Dict[str, Any], *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {}
