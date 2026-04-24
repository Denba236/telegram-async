"""
Workflow Manager - Manages workflow execution and node connections
Similar to n8n workflow orchestrator
"""

from typing import Dict, List, Any, Optional
from .nodes import WorkflowNode, NodeType, NODE_TYPES
import uuid
import json


class Workflow:
    """Represents a complete workflow with nodes and connections"""
    
    def __init__(self, workflow_id: str, name: str, description: str = ""):
        self.workflow_id = workflow_id
        self.name = name
        self.description = description
        self.nodes: Dict[str, WorkflowNode] = {}
        self.connections: Dict[str, List[str]] = {}  # node_id -> [connected_node_ids]
        self.entry_points: List[str] = []  # Node IDs where execution starts
        
    def add_node(self, node: WorkflowNode) -> None:
        """Add a node to the workflow"""
        self.nodes[node.node_id] = node
        if node.type == NodeType.INPUT:
            self.entry_points.append(node.node_id)
    
    def connect_nodes(self, from_node_id: str, to_node_id: str) -> None:
        """Connect two nodes together"""
        if from_node_id not in self.connections:
            self.connections[from_node_id] = []
        self.connections[from_node_id].append(to_node_id)
        self.nodes[from_node_id].connections.append(to_node_id)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the workflow with given input data"""
        if not self.entry_points:
            raise ValueError("No entry points defined in workflow")
        
        print(f"\n{'='*50}")
        print(f"Starting Workflow: {self.name}")
        print(f"{'='*50}\n")
        
        current_data = input_data.copy()
        visited_nodes = set()
        
        # Start from entry points
        nodes_to_process = list(self.entry_points)
        
        while nodes_to_process:
            node_id = nodes_to_process.pop(0)
            
            if node_id in visited_nodes:
                continue
            
            if node_id not in self.nodes:
                print(f"[Warning] Node {node_id} not found, skipping")
                continue
            
            node = self.nodes[node_id]
            
            # Execute node
            try:
                current_data = await node.execute(current_data)
                visited_nodes.add(node_id)
                print(f"✓ Node '{node.name}' executed successfully\n")
            except Exception as e:
                print(f"✗ Error executing node '{node.name}': {e}")
                current_data["error"] = str(e)
                return current_data
            
            # Add connected nodes to processing queue
            if node_id in self.connections:
                connected = self.connections[node_id]
                
                # Handle conditional branching
                if node.type == NodeType.CONDITION:
                    condition_result = current_data.get("condition_result", False)
                    true_node = node.config.get("true_node")
                    false_node = node.config.get("false_node")
                    
                    next_node = true_node if condition_result else false_node
                    if next_node:
                        nodes_to_process.append(next_node)
                else:
                    nodes_to_process.extend(connected)
        
        print(f"\n{'='*50}")
        print(f"Workflow Complete")
        print(f"{'='*50}\n")
        
        return current_data
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize workflow to dict"""
        return {
            "id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "connections": self.connections,
            "entry_points": self.entry_points
        }
    
    def to_json(self) -> str:
        """Serialize workflow to JSON"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workflow':
        """Deserialize workflow from dict"""
        workflow = cls(data["id"], data["name"], data.get("description", ""))
        
        # Recreate nodes
        for node_id, node_data in data["nodes"].items():
            node = WorkflowNode.from_dict(node_data)
            workflow.nodes[node_id] = node
        
        # Restore connections
        workflow.connections = data.get("connections", {})
        workflow.entry_points = data.get("entry_points", [])
        
        return workflow
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Workflow':
        """Deserialize workflow from JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class WorkflowManager:
    """Manages multiple workflows and provides execution context"""
    
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        
    def create_workflow(self, name: str, description: str = "") -> Workflow:
        """Create a new workflow"""
        workflow_id = str(uuid.uuid4())
        workflow = Workflow(workflow_id, name, description)
        self.workflows[workflow_id] = workflow
        return workflow
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get workflow by ID"""
        return self.workflows.get(workflow_id)
    
    def list_workflows(self) -> List[Dict[str, str]]:
        """List all workflows"""
        return [
            {"id": wf.workflow_id, "name": wf.name, "description": wf.description}
            for wf in self.workflows.values()
        ]
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow"""
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]
            return True
        return False
    
    async def execute_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow by ID"""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return {"error": f"Workflow {workflow_id} not found"}
        
        return await workflow.execute(input_data)
    
    def export_workflow(self, workflow_id: str) -> str:
        """Export workflow as JSON"""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return ""
        return workflow.to_json()
    
    def import_workflow(self, json_str: str) -> Workflow:
        """Import workflow from JSON"""
        workflow = Workflow.from_json(json_str)
        self.workflows[workflow.workflow_id] = workflow
        return workflow


# Global workflow manager instance
workflow_manager = WorkflowManager()
