import inspect
from typing import Any, Dict, List, Optional, Tuple, Set


class NodeDict(dict):
    """Dictionary subclass that returns all values when called as a function, e.g., nodes()."""
    def __call__(self) -> List[Any]:
        return list(self.values())


class Graph:
    """
    Directed Acyclic Graph (DAG) engine for QVEX pipelines.
    Enhanced to manage and propagate global Substrate Context (homogeneity invariants,
    topological circulation sums, and charge neutrality constraints) across nodes.
    """
    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        self.name = name or "QVEX_Computational_Graph"
        self.config = kwargs
        self.nodes = NodeDict()
        # Edges stored as: (src_node, src_port, dst_node, dst_port)
        self.edges: Set[Tuple[str, str, str, str]] = set()

    def add_node(self, node: Any, name: Optional[str] = None) -> Any:
        node_id = name or getattr(node, "node_id", None) or getattr(node, "name", None) or str(node)
        if node_id in self.nodes:
            raise ValueError(f"duplicate node detected: {node_id}")
        if hasattr(node, "node_id") and not getattr(node, "name", None):
            node.name = node_id
        self.nodes[node_id] = node
        return node

    def connect(self, src: str, src_port: str, dst: str, dst_port: str) -> None:
        if src not in self.nodes:
            raise KeyError(f"Source node not found: {src}")
        if dst not in self.nodes:
            raise KeyError(f"Destination node not found: {dst}")
        self.edges.add((src, src_port, dst, dst_port))

    def add_edge(self, src: str, src_port: str, dst: str, dst_port: str) -> None:
        self.connect(src, src_port, dst, dst_port)

    def _order(self) -> List[str]:
        """Kahn's topological sort algorithm with cycle detection."""
        in_degree = {nid: 0 for nid in self.nodes}
        adj = {nid: [] for nid in self.nodes}

        for src, _, dst, _ in self.edges:
            if src in adj and dst in in_degree:
                adj[src].append(dst)
                in_degree[dst] += 1

        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        ordered = []

        while queue:
            curr = queue.pop(0)
            ordered.append(curr)
            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        if len(ordered) != len(self.nodes):
            raise ValueError("cycle detected in computational graph")
        return ordered

    def run(self, initial_inputs: Optional[Dict[str, Dict[str, Any]]] = None, substrate_ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
        """
        Executes the computational graph in topological order.
        Maintains and propagates global substrate invariants across nodes.
        """
        initial_inputs = initial_inputs or {}

        if substrate_ctx is None:
            substrate_ctx = {
                "rho_0": 1.0,           # Uniform homogeneous substrate density
                "global_charge_sum": 0.0, # Enforcing sum(q_i) = 0 topological balance
                "topological_flux_quantum": 1.0
            }

        ordered_nodes = self._order()
        node_outputs: Dict[str, Dict[str, Any]] = {}

        # Pre-populate outputs with initial external inputs (node_id -> port_dict)
        for nid, ports in initial_inputs.items():
            node_outputs[nid] = dict(ports)

        # Build incoming edge map: dst -> list of (src, src_port, dst_port)
        incoming_edges: Dict[str, List[Tuple[str, str, str]]] = {nid: [] for nid in self.nodes}
        for src, src_port, dst, dst_port in self.edges:
            incoming_edges[dst].append((src, src_port, dst_port))

        for nid in ordered_nodes:
            node = self.nodes[nid]
            current_inputs = dict(node_outputs.get(nid, {}))

            for src, src_port, dst_port in incoming_edges[nid]:
                if src not in node_outputs:
                    raise KeyError(f"missing output from source node '{src}' for target '{nid}'")
                src_outputs = node_outputs[src]
                if src_port not in src_outputs:
                    raise KeyError(f"missing output port '{src_port}' on node '{src}'")
                current_inputs[dst_port] = src_outputs[src_port]

            # Safe execution handling signature compatibility
            if hasattr(node, "execute"):
                try:
                    sig = inspect.signature(node.execute)
                    has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
                    if "substrate_ctx" in sig.parameters or has_var_kw:
                        outputs = node.execute(current_inputs, substrate_ctx=substrate_ctx)
                    else:
                        outputs = node.execute(current_inputs)
                except Exception:
                    outputs = node.execute(current_inputs)
            elif hasattr(node, "compute"):
                try:
                    sig = inspect.signature(node.compute)
                    has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
                    if "substrate_ctx" in sig.parameters or has_var_kw:
                        outputs = node.compute(current_inputs, substrate_ctx=substrate_ctx)
                    else:
                        outputs = node.compute(current_inputs)
                except Exception:
                    outputs = node.compute(current_inputs)
            elif callable(node):
                outputs = node(current_inputs)
            else:
                raise TypeError(f"Node {nid} is not executable.")

            node_outputs[nid] = outputs if isinstance(outputs, dict) else {"result": outputs}

        return node_outputs

    def execute(self, initial_inputs: Optional[Dict[str, Dict[str, Any]]] = None, substrate_ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
        return self.run(initial_inputs=initial_inputs, substrate_ctx=substrate_ctx)


ComputationalGraph = Graph
