from utils.schema import ReactionState as State
from langgraph.types import interrupt
from utils.schema import HumanFeedback as FeedbackClass
from typing import Literal

def build_pre_payload(state:State):
    canonical_smiles_input = state.get("canonical_smiles","")
    conditions = state.get("conditions",{})
    retrived_context = state.get("retrieved_context",[])
    Warning = state.get("warnings",[])
    
    if not retrived_context:
        retrived_context = ["No document is provided by you"]
        
    return {
        "mode":"pre_prediction",
        "canonical_smiles":canonical_smiles_input,
        "conditions":conditions,
        "retrieved_context":retrived_context,
        "warnings":Warning,
        "actions": ["approve","modify","reject"]
    }

def build_post_payload(state:State):
    predictions = state.get("prediction","")
    confidence_retrived = state.get("confidence",0.0)
    mechanism_retrived = state.get("mechanism","")
    prediction_metadata = state.get("prediction_metadata",{})
    validation_results = state.get("validation_results",{})
    validation_scores = state.get("validation_scores",{})
    retry_counts = state.get("retry_count",{})
    

    return {
        "mode":"post_prediction",
        "prediction":predictions,
        "confidence":confidence_retrived,
        "mechanism":mechanism_retrived,
        "prediction_metadata":prediction_metadata,
        "validation_results":validation_results,
        "validation_scores":validation_scores,
        "retry_counts":retry_counts,
        "actions":["approve","modify","reject","retry"]
    }


def update_human_feed_back(state: State,response : FeedbackClass):
    state["human_feedback"] = response
    


def human_review_agent(state:State, mode: Literal["pre_prediction", "post_prediction"]):
    if mode == "pre_prediction":
        payload =  build_pre_payload(state)
    elif mode == "post_prediction":
        payload =  build_post_payload(state)
    else:
        raise ValueError(f"Invalid mode: {mode}")

    human_response = interrupt(payload)
    
    
    #  reponse validation
    valid_decision = ["approve","modify","reject","retry"]
    decision = human_response["decision"] 
    if decision not in valid_decision:
        raise ValueError(f"Invalid decision: {human_response['decision']}")
    
    #  update the state fun 
    update_human_feed_back(state,{
        "mode":mode,
        "decision":human_response["decision"],
        "comment":human_response.get("comment",""),
        "edited_fields":human_response.get("edited_fields",{})
    })
    
    return state

