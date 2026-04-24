"""
Workflow Storage - Persistent storage for workflows using database
"""

import json
from typing import Dict, List, Optional
from .manager import Workflow


class WorkflowStorage:
    """Manages persistent storage of workflows"""
    
    def __init__(self):
        self.workflows_db: Dict[str, Dict] = {}
        self.user_preferences: Dict[int, Dict] = {}
    
    def save_workflow(self, workflow: Workflow) -> bool:
        """Save workflow to storage"""
        try:
            self.workflows_db[workflow.workflow_id] = {
                "data": workflow.to_dict(),
                "json": workflow.to_json()
            }
            return True
        except Exception as e:
            print(f"[Storage] Error saving workflow: {e}")
            return False
    
    def load_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Load workflow from storage"""
        if workflow_id in self.workflows_db:
            wf_data = self.workflows_db[workflow_id]
            return Workflow.from_json(wf_data["json"])
        return None
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete workflow from storage"""
        if workflow_id in self.workflows_db:
            del self.workflows_db[workflow_id]
            return True
        return False
    
    def list_workflows(self) -> List[Dict]:
        """List all stored workflows"""
        return [
            {
                "id": wf_id,
                "name": wf_data["data"]["name"],
                "description": wf_data["data"].get("description", "")
            }
            for wf_id, wf_data in self.workflows_db.items()
        ]
    
    def export_workflow(self, workflow_id: str) -> str:
        """Export workflow as JSON string"""
        if workflow_id in self.workflows_db:
            return self.workflows_db[workflow_id]["json"]
        return ""
    
    def import_workflow(self, json_str: str) -> Optional[Workflow]:
        """Import workflow from JSON string"""
        try:
            workflow = Workflow.from_json(json_str)
            self.save_workflow(workflow)
            return workflow
        except Exception as e:
            print(f"[Storage] Error importing workflow: {e}")
            return None
    
    def save_user_preferences(self, user_id: int, preferences: Dict) -> bool:
        """Save user preferences"""
        try:
            self.user_preferences[user_id] = preferences
            return True
        except Exception as e:
            print(f"[Storage] Error saving preferences: {e}")
            return False
    
    def get_user_preferences(self, user_id: int) -> Dict:
        """Get user preferences"""
        return self.user_preferences.get(user_id, {})
    
    def get_user_workflows(self, user_id: int) -> List[Dict]:
        """Get all workflows for a specific user"""
        user_prefs = self.get_user_preferences(user_id)
        user_workflow_ids = user_prefs.get("workflows", [])
        
        return [
            {
                "id": wf_id,
                "name": self.workflows_db[wf_id]["data"]["name"],
                "description": self.workflows_db[wf_id]["data"].get("description", "")
            }
            for wf_id in user_workflow_ids
            if wf_id in self.workflows_db
        ]
    
    def add_user_workflow(self, user_id: int, workflow_id: str) -> bool:
        """Add workflow to user's list"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {"workflows": []}
        
        if "workflows" not in self.user_preferences[user_id]:
            self.user_preferences[user_id]["workflows"] = []
        
        if workflow_id not in self.user_preferences[user_id]["workflows"]:
            self.user_preferences[user_id]["workflows"].append(workflow_id)
            return True
        return False


# Global storage instance
workflow_storage = WorkflowStorage()
