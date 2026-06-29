from langchain.agents.middleware import HumanInTheLoopMiddleware 
from utils.schema import ReactionState as State


MIN_CONFIDENCE_THRESHOLD = 0.60
MAX_PREDICTOR_RETRIES = 3
MAX_VERIFIER_RETRIES = 2


#  ROUTING FUNCTION 
def require_human_review(state: State) -> bool:

    scores = state.get("validation_scores", {})
    results = state.get("validation_results", {})
    confidence = state.get("confidence", 0)

    retries = state.get("retry_count", {})

    predictor_retry = retries.get("predictor", 0)
    verifier_retry = retries.get("verifier", 0)

    # Product validation failed after all retries exhausted

    if (
        not results.get("product_validation", True)
        and predictor_retry >= MAX_PREDICTOR_RETRIES
        and verifier_retry >= MAX_VERIFIER_RETRIES
    ):
        return True

    # Low confidence after predictor retries exhausted

    if (
        confidence < MIN_CONFIDENCE_THRESHOLD
        and predictor_retry >= MAX_PREDICTOR_RETRIES
    ):
        return True

    # Context validation failed after verifier retries exhausted

    if (
        scores.get("context_score", 1.0) < 0.35
        and verifier_retry >= MAX_VERIFIER_RETRIES
    ):
        return True

    # Mechanism validation failed after verifier retries exhausted

    if (
        scores.get("mechanism_score", 1.0) < 0.20
        and verifier_retry >= MAX_VERIFIER_RETRIES
    ):
        return True

    return False



HumanInTheLoopMiddleware(
    interrupt_on={
        
    }
)