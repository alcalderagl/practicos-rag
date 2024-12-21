from pydantic import BaseModel


class ChatHistory(BaseModel):
    """
    Represents a single entry in a chat history.

    Attributes
    ----------
    role : str
        The role of the person in the chat (e.g., 'user', 'assistant').
    message : str
        The message sent by the person with the specified role.
    """

    role: str
    message: str
