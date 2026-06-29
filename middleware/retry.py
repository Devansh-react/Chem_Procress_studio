from utils.schema import ReactionState as State

# Predictor retries

MAX_PREDICTOR_RETRIES = 3

# Retriever retries

MAX_RETRIEVER_RETRIES = 2

# Verifier retries

MAX_VERIFIER_RETRIES = 2

# Supervisor retries

MAX_WORKFLOW_RETRIES = 5

def should_retry_prediction(state: State) -> bool:

    results = state.get("validation_results")
    retry_count = state.get("retry_count",{0})

    if not results:
        return False

    if retry_count["predictor"] >= MAX_PREDICTOR_RETRIES:
        return False

    if not results.get("product_validation", True):
        return True

    if not results.get("mechanism_validation", True):
        return True

    if not results.get("retrieved_context_validation", True):
        return True

    return False

middleware_verifier = should_retry_prediction
