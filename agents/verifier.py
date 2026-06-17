from dataclasses import dataclass

from tools.chemistry.RDKit_tool import validate_smiles
from utils.schemas_chat import ReactionState as State
from tools.verification.Context_verifier import verify_prediction_with_context
from tools.verification.mechaism_verifier import validate_mechanism

@dataclass
class validation_results:
    smiles_validation:bool
    retrieved_context_validation:bool
    mechanism_validation:bool
    
    
def verifier_agent(state:State, validation_results:validation_results):

# validate the smiles using RDKit
    output = state.get("prediction")
    if not output:
        validation_results.smiles_validation = False
        return validation_results
    
    validation_result_1= validate_smiles(output)
    if not validation_result_1["is_valid"]:
        validation_results.smiles_validation = False
    else :
        validation_results.smiles_validation = True
        
#  validation the smiles using the retrieved document context and c onfidence score 
    prediction_mechanism = state.get("mechanism") or ""
    retrived_context = state.get("retrieved_context", [])
    confidence = state.get("confidence", 0.0)
    raw_score = verify_prediction_with_context(prediction_mechanism, retrived_context,confidence)
    
    if isinstance(raw_score,float):
        score = raw_score
    else:
        score = 0.0
    
    if score < 0.25:
        validation_results.retrieved_context_validation = False
    else:
        validation_results.retrieved_context_validation = True
        
    rectant  = state.get("canonical_smiles") or state.get("smiles") or ""
    
    condition = state.get("conditions",{})
    
    mechanism_result = validate_mechanism(rectant, condition, prediction_mechanism, output, retrived_context)
    
    if mechanism_result < 0.5:
        validation_results.mechanism_validation = False
    else:
        validation_results.mechanism_validation = True
    
    
    
    
    
    
    
    
    # {
#     "smiles": "CCBr",
#     "canonical_smiles": "CCBr",
#     "conditions": {
#         "reagent": "NaOH"
#     },

#     "retrieved_context": [...],

#     "prediction": "CCOH",
#     "confidence": 0.85,
#     "mechanism": "SN2",
#     "prediction_metadata": {...}
# }
    

    
    
    