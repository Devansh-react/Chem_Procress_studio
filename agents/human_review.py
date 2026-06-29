from middleware.interrupts import require_human_review as human_review 
from utils.schema import ReactionState as State


def build_pre_payload(state:State):
    smiles_input = state.get("canonical_smiles","smiles")
    conditions = state.get("conditions",{})
    retrived_context = state.get("retrieved_context",[])
    Warning = state.get("warnings",[])
    
    if not retrived_context:
        retrived_context = ["No document is provided by you"]
        
    return {
        "smiles":smiles_input,
        "conditions":conditions,
        "retrieved_context":retrived_context,
        "warnings":Warning
    }

def build_post_payload(state:State):
    predictions = state.get("prediction","")
    confidence_retrived = state.get("confidence",0.0)
    mechanism_retrived = state.get("mechanism","")
    prediction_metadata = state.get("prediction_metadata",{})
    validation_results = state.get("validation_results",{})
    validation_scores = state.get("validation_scores",{})
    retry_counts = state.get("retry_count",{});

    return {
        "prediction":predictions,
        "confidence":confidence_retrived,
        "mechanism":mechanism_retrived,
        "prediction_metadata":prediction_metadata,
        "validation_results":validation_results,
        "validation_scores":validation_scores,
        "retry_counts":retry_counts
    }


def update_State():
    pass


def human_review_agent(stae:State):
    pass

