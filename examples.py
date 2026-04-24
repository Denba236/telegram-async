"""
Example workflows - Pre-built translation pipelines
"""

from .manager import Workflow, workflow_manager
from .nodes import (
    InputNode,
    DetectLanguageNode,
    TranslateNode,
    TransformNode,
    ConditionNode,
    OutputNode
)


def create_simple_translation_workflow(source_lang: str = "auto", target_lang: str = "en") -> Workflow:
    """Create a simple translation workflow"""
    
    workflow = workflow_manager.create_workflow(
        f"Simple Translation ({source_lang} → {target_lang})",
        f"Basic translation from {source_lang} to {target_lang}"
    )
    
    # Create nodes
    input_node = InputNode("input")
    translate_node = TranslateNode("translate")
    translate_node.config["source_lang"] = source_lang
    translate_node.config["target_lang"] = target_lang
    translate_node.config["use_ai"] = True
    output_node = OutputNode("output")
    
    # Add nodes to workflow
    workflow.add_node(input_node)
    workflow.add_node(translate_node)
    workflow.add_node(output_node)
    
    # Connect nodes
    workflow.connect_nodes("input", "translate")
    workflow.connect_nodes("translate", "output")
    
    return workflow


def create_advanced_translation_workflow() -> Workflow:
    """Create advanced workflow with language detection and transformation"""
    
    workflow = workflow_manager.create_workflow(
        "Advanced Translation Pipeline",
        "Auto-detect language, translate to English, and format output"
    )
    
    # Create nodes
    input_node = InputNode("input")
    detect_node = DetectLanguageNode("detect")
    translate_node = TranslateNode("translate")
    translate_node.config["source_lang"] = "auto"
    translate_node.config["target_lang"] = "en"
    translate_node.config["use_ai"] = True
    transform_node = TransformNode("transform")
    transform_node.config["operation"] = "capitalize"
    output_node = OutputNode("output")
    output_node.config["format"] = "markdown"
    
    # Add nodes
    workflow.add_node(input_node)
    workflow.add_node(detect_node)
    workflow.add_node(translate_node)
    workflow.add_node(transform_node)
    workflow.add_node(output_node)
    
    # Connect nodes in sequence
    workflow.connect_nodes("input", "detect")
    workflow.connect_nodes("detect", "translate")
    workflow.connect_nodes("translate", "transform")
    workflow.connect_nodes("transform", "output")
    
    return workflow


def create_conditional_workflow() -> Workflow:
    """Create workflow with conditional branching"""
    
    workflow = workflow_manager.create_workflow(
        "Conditional Translation",
        "Translate only if text is in Polish, otherwise pass through"
    )
    
    # Create nodes
    input_node = InputNode("input")
    detect_node = DetectLanguageNode("detect")
    
    translate_node = TranslateNode("translate")
    translate_node.config["source_lang"] = "pl"
    translate_node.config["target_lang"] = "en"
    translate_node.config["use_ai"] = True
    
    passthrough_node = TransformNode("passthrough")
    passthrough_node.config["operation"] = "trim"
    
    condition_node = ConditionNode("condition")
    condition_node.config["condition"] = "language_equals"
    condition_node.config["value"] = "pl"
    condition_node.config["true_node"] = "translate"
    condition_node.config["false_node"] = "passthrough"
    
    output_node = OutputNode("output")
    
    # Add nodes
    workflow.add_node(input_node)
    workflow.add_node(detect_node)
    workflow.add_node(translate_node)
    workflow.add_node(passthrough_node)
    workflow.add_node(condition_node)
    workflow.add_node(output_node)
    
    # Connect nodes
    workflow.connect_nodes("input", "detect")
    workflow.connect_nodes("detect", "condition")
    # Conditional connections are handled in config
    workflow.connect_nodes("translate", "output")
    workflow.connect_nodes("passthrough", "output")
    
    return workflow


def create_multistage_workflow() -> Workflow:
    """Create multi-stage workflow: detect → translate → transform → output"""
    
    workflow = workflow_manager.create_workflow(
        "Multi-Stage Translation",
        "Detect → Translate to Polish → Uppercase → Output"
    )
    
    # Create nodes
    input_node = InputNode("input")
    detect_node = DetectLanguageNode("detect")
    translate_node = TranslateNode("translate")
    translate_node.config["source_lang"] = "auto"
    translate_node.config["target_lang"] = "pl"
    translate_node.config["use_ai"] = True
    transform_node = TransformNode("transform")
    transform_node.config["operation"] = "uppercase"
    output_node = OutputNode("output")
    output_node.config["format"] = "text"
    
    # Add nodes
    workflow.add_node(input_node)
    workflow.add_node(detect_node)
    workflow.add_node(translate_node)
    workflow.add_node(transform_node)
    workflow.add_node(output_node)
    
    # Connect in sequence
    workflow.connect_nodes("input", "detect")
    workflow.connect_nodes("detect", "translate")
    workflow.connect_nodes("translate", "transform")
    workflow.connect_nodes("transform", "output")
    
    return workflow


def initialize_example_workflows():
    """Create and register all example workflows"""
    
    workflows = [
        create_simple_translation_workflow(),
        create_advanced_translation_workflow(),
        create_conditional_workflow(),
        create_multistage_workflow(),
    ]
    
    print(f"✅ Initialized {len(workflows)} example workflows")
    return workflows
