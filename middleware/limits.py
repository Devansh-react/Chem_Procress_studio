from langchain.agents.middleware import ModelCallLimitMiddleware,ToolCallLimitMiddleware

#  MODEL LIMIT 
Model_middleware = ModelCallLimitMiddleware(
    thread_limit=10,
    run_limit=2,
    exit_behavior="end"
)

#  global limit FOR TOOLS 
tool_middleware = ToolCallLimitMiddleware(
    thread_limit=10,
    run_limit= None,    
)


# tools_retry in v2 version 
#  models retry 
#  model fall back 