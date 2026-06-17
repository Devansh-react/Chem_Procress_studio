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

from tools.chemistry.RDKit_tool import validate_smiles
from utils.schemas_chat import ReactionState as State

class validation_results:
    smiles_validation:bool
    retrieved_context_validation:bool
    
    
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

    
    
    