from typing import TypedDict, List, Dict, Optional, Literal, Any


class HumanFeedback(TypedDict):
    required:bool 
    
    mode: Literal[
        "pre_prediction",
        "post_prediction"
    ]
    
    decision : Literal[
        "approve",
        "reject",
        "retry",
        "modify"
    ]
    
    comment: Optional[str]
    
    edited_feilds : Dict[str,Any]
    
    


class ReactionState(TypedDict):
    user_query: str
    task_type: Literal["predict", "Validate", "literature_review", "explain", "report"]
    
    
    smiles: str
    canonical_smiles: Optional[str]
    conditions: Dict[str, str]
    
    uploaded_docs: Optional[List[str]]
    pdf_injested: bool
    external_doc_available: bool
    retrieved_context: List[Dict[str, Any]]
    
    
    prediction: Optional[str]
    confidence: float
    mechanism: Optional[str]
    prediction_metadata: Optional[Dict[str, str]]
    
    
    validation_results: Dict[str, bool]
    validation_scores: Dict[str, float]
    
    
    human_feedback: HumanFeedback
    
    explanation_report: Optional[str]
    warnings:List[str]
    
    
    retry_count: Dict[
        Literal[
            "predictor",
            "retriever",
            "verifier",
            "workflow"
        ],
        int
    ]
    # prefictor returiver and verifier count  model count 
    
    status: Literal[
        "initialized",
        "validated",
        "retrieved",
        "predicted",
        "verified",
        "human_review",
        "completed",
        "failed"
    ]
    
    
    #  conversational history
    messages:Optional[List[str]]
