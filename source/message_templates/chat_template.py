from schemas.messages import Message

def FORMAT_CHAT_TEMPLATE(immediate_context_string = None, retrieved_context_string = None):
    MAIN_MSG = "You are a helpful assistant chatting with the user. Try to answer questions to the best of your ability."

    if immediate_context_string:
        MAIN_MSG = MAIN_MSG + f"\nBelow is the document you are currently discussing:  \n {immediate_context_string}"
    
    if retrieved_context_string:
        MAIN_MSG = MAIN_MSG + f"\nBelow are references which may or may not be useful to you. If they help assist the user, please quote them in your replies! \n {retrieved_context_string}"

    return Message(role="system", content=MAIN_MSG)