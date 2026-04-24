"""
n8n-like Translation Workflow Engine
Visual workflow builder for AI-powered translations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum
import json


class NodeType(Enum):
    """Types of workflow nodes"""
    INPUT = "input"
    DETECT_LANGUAGE = "detect_language"
    TRANSLATE = "translate"
    TRANSFORM = "transform"
    CONDITION = "condition"
    OUTPUT = "output"
    CUSTOM = "custom"


class WorkflowNode(ABC):
    """Base class for workflow nodes"""
    
    def __init__(self, node_id: str, name: str, node_type: NodeType):
        self.node_id = node_id
        self.name = name
        self.type = node_type
        self.config: Dict[str, Any] = {}
        self.connections: List[str] = []  # IDs of connected nodes
        
    @abstractmethod
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute node logic"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize node to dict"""
        return {
            "id": self.node_id,
            "name": self.name,
            "type": self.type.value,
            "config": self.config,
            "connections": self.connections
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowNode':
        """Deserialize node from dict"""
        node_type = NodeType(data["type"])
        node_class = NODE_TYPES[node_type]
        node = node_class(data["id"], data["name"], node_type)
        node.config = data.get("config", {})
        node.connections = data.get("connections", [])
        return node


class InputNode(WorkflowNode):
    """Input node - receives text to translate"""
    
    def __init__(self, node_id: str, name: str = "Input"):
        super().__init__(node_id, name, NodeType.INPUT)
        
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Return input data"""
        print(f"[Input Node] Processing input")
        return data


class DetectLanguageNode(WorkflowNode):
    """Detect language of input text"""
    
    def __init__(self, node_id: str, name: str = "Detect Language"):
        super().__init__(node_id, name, NodeType.DETECT_LANGUAGE)
        
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect language using simple heuristics or AI"""
        text = data.get("text", "")
        
        # Simple language detection (can be replaced with AI)
        detected_lang = self._detect_language(text)
        data["detected_language"] = detected_lang
        
        print(f"[Detect Language] Detected: {detected_lang}")
        return data
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection based on characters"""
        text_lower = text.lower()
        
        # Polish indicators
        polish_chars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż']
        if any(char in text_lower for char in polish_chars):
            return "pl"
        
        # English indicators
        common_english = ['the', 'is', 'are', 'was', 'were', 'have', 'has']
        if any(word in text_lower.split() for word in common_english):
            return "en"
        
        # Default to English
        return "en"


class TranslateNode(WorkflowNode):
    """Translate text using OpenRouter AI"""
    
    def __init__(self, node_id: str, name: str = "Translate"):
        super().__init__(node_id, name, NodeType.TRANSLATE)
        self.config = {
            "source_lang": "auto",
            "target_lang": "en",
            "use_ai": True
        }
        
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate text"""
        text = data.get("text", "")
        source_lang = data.get("detected_language", "en") if self.config["source_lang"] == "auto" else self.config["source_lang"]
        target_lang = self.config.get("target_lang", "en")
        
        if source_lang == target_lang:
            print(f"[Translate] Same language, skipping")
            data["translated_text"] = text
            return data
        
        # Use AI translation if enabled
        if self.config.get("use_ai", True):
            translated = await self._translate_with_ai(text, source_lang, target_lang)
        else:
            translated = self._simple_translate(text, source_lang, target_lang)
        
        data["translated_text"] = translated
        data["source_language"] = source_lang
        data["target_language"] = target_lang
        
        print(f"[Translate] {source_lang} -> {target_lang}")
        return data
    
    async def _translate_with_ai(self, text: str, source: str, target: str) -> str:
        """Translate using OpenRouter AI"""
        try:
            from my_proj.telegram_async.openrouter_client import openrouter_client
            
            prompt = f"""Translate the following text from {source} to {target}.
Return ONLY the translated text, nothing else.

Text: {text}"""
            
            response = await openrouter_client.generate(prompt)
            return response.strip()
        except Exception as e:
            print(f"[AI Translation Error] {e}")
            return self._simple_translate(text, source, target)
    
    def _simple_translate(self, text: str, source: str, target: str) -> str:
        """Simple dictionary-based translation (fallback)"""
        # This is a placeholder - in real use, always use AI
        return f"[Translated to {target}] {text}"


class TransformNode(WorkflowNode):
    """Transform/modify text"""
    
    def __init__(self, node_id: str, name: str = "Transform"):
        super().__init__(node_id, name, NodeType.TRANSFORM)
        self.config = {
            "operation": "uppercase"  # uppercase, lowercase, capitalize, trim
        }
        
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform text"""
        text = data.get("translated_text", data.get("text", ""))
        operation = self.config.get("operation", "uppercase")
        
        if operation == "uppercase":
            text = text.upper()
        elif operation == "lowercase":
            text = text.lower()
        elif operation == "capitalize":
            text = text.title()
        elif operation == "trim":
            text = text.strip()
        
        data["transformed_text"] = text
        print(f"[Transform] Applied: {operation}")
        return data


class ConditionNode(WorkflowNode):
    """Conditional branching"""
    
    def __init__(self, node_id: str, name: str = "Condition"):
        super().__init__(node_id, name, NodeType.CONDITION)
        self.config = {
            "condition": "language_equals",
            "value": "en",
            "true_node": None,
            "false_node": None
        }
        
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate condition and route accordingly"""
        condition = self.config.get("condition", "")
        value = self.config.get("value", "")
        
        result = False
        
        if condition == "language_equals":
            detected_lang = data.get("detected_language", "")
            result = detected_lang == value
        
        elif condition == "contains_word":
            text = data.get("text", "")
            result = value.lower() in text.lower()
        
        elif condition == "length_greater":
            text = data.get("text", "")
            result = len(text) > int(value)
        
        data["condition_result"] = result
        branch = "true" if result else "false"
        
        print(f"[Condition] {condition}: {result} -> {branch}")
        return data


class OutputNode(WorkflowNode):
    """Output node - sends final result"""
    
    def __init__(self, node_id: str, name: str = "Output"):
        super().__init__(node_id, name, NodeType.OUTPUT)
        self.config = {
            "format": "text"  # text, markdown, html
        }
        
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format and return output"""
        text = data.get("transformed_text", data.get("translated_text", data.get("text", "")))
        
        format_type = self.config.get("format", "text")
        if format_type == "uppercase":
            text = text.upper()
        elif format_type == "markdown":
            text = f"```\n{text}\n```"
        
        data["final_output"] = text
        print(f"[Output] Final result ready")
        return data


# Registry of node types
NODE_TYPES = {
    NodeType.INPUT: InputNode,
    NodeType.DETECT_LANGUAGE: DetectLanguageNode,
    NodeType.TRANSLATE: TranslateNode,
    NodeType.TRANSFORM: TransformNode,
    NodeType.CONDITION: ConditionNode,
    NodeType.OUTPUT: OutputNode,
}
