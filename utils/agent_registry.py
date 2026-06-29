from agents.validator import validate_agent as Validator
from agents.retriever import retriever_agent as Reteriver_Agent 
from agents.explainer import explainer_agent as explainer
from agents.predictor import predict_reaction as predictor
from agents.verifier import verifier_agent as verifier
from prompts import Validator_prompt , Retriever_prompt,explainer_prompt , prediction_prompt ,verifier_prompt

from tools.retrieval.RAG_tool import retrieve_context as simlarity_search , retrieve_context_mmr as mmr_search 
from tools.chemistry import RDKit_tool
from tools.prediction.Rxn_predict_tool import ReactionPredictor
from tools.verification.Context_verifier import verify_prediction_with_context as context_verifier
from tools.verification.mechaism_verifier import validate_mechanism



from middleware.retry import middleware_verifier
from middleware.limits import tool_middleware as limits , Model_middleware as model 
from middleware.interrupts import require_human_review 






AGENT_REGISTORY = {
    "validator": {
        "description": "This agent validates the SMILES input using RDKit",
        "agent" : Validator ,
        "Prompt" : Validator_prompt,
        "tools":[RDKit_tool],
        "middleware": [middleware_verifier, limits , model]
    },
    "retriever":{
        "description":"This agent retrived the additional information from the uploaded dcuments RAG",
        "agent":Reteriver_Agent,
        "Prompt": Retriever_prompt,
        "tools":[simlarity_search,mmr_search],
        "middleware":[middleware_verifier, limits , model]
    },
    "explainer":{
        "description":"This agent is responsible to explain the result to user in easy redeable format along with all the data",
        "agent":explainer,
        "Prompt": explainer_prompt,
        "tools":[],
        "middleware":[middleware_verifier, limits , model]
    },
    "predictor":{
        "description":"This agent predict the product of the reaction along with the mechanism and confidence score",
        "agent": predictor,
        "Prompt":prediction_prompt,
        "tools":[ReactionPredictor],
        "middleware":[middleware_verifier, limits , model]
    },
    "verifier":{
        "description":"It verifies the predicted output by Smiles  Validation, context validation and mechanism validation",
        "agent":verifier, # function name
        "Prompt": verifier_prompt,
        "tools":[RDKit_tool,context_verifier,validate_mechanism],
        "middleware":[limits , model]
    },
    "human_review":{
        "description":"",
        "agent":"",
        "Prompt":"",
        "tools":[],
        
    }
    
}