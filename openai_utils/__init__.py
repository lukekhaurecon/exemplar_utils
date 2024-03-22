"""
These utils should make it easier to construct chat completions
"""
from enum import Enum
from typing import Optional
from openai import AzureOpenAI
from pydantic import BaseModel, field_validator, ValidationInfo

class Role(Enum):
    """The different roles available to the OpenAI API"""
    assistant: str  = "assistant"
    function: str   = "function"
    system: str     = "system"
    user: str       = "user"


class Message(BaseModel):
    """A chat message"""
    role: Role
    content: str
    # Optional data for function calls
    name: Optional[str] = None

    @field_validator('name')
    @classmethod
    def check_valid_name(cls, v: Optional[str], info: ValidationInfo) -> str:
        """Make sure function messages have a name"""
        if (info.data.get("role") is Role.function) and (v is None):
            raise ValueError('a function message requires the name field to be defined')
        return v

    def format(self):
        """Format message for OpenAI json serializable object"""
        if self.role is Role.function:
            return {
                "role": self.role.value,
                "tool_call_id": f"call_{self.name}",
                "name": self.name,
                "content": self.content,
            }
        else:
            return {
                "role": self.role.value,
                "content": self.content
            }


class Messages(list[Message]):
    """OpenAI messages"""
    def format(self):
        """Format messages for OpenAI json serializable object"""
        return [
            msg.format() for msg in self
        ]

    def __add__(self, other: "Messages"):
        return Messages([*self] + [*other])


class ChatClient:
    """
    House the functionality in a convenience class
    """
    # This system message can alter the behaviour of the chatbot
    # and will not be displayed to users
    SYSTEM_MESSAGE = Message(
        role=Role.system,
        content=(
            "You are a helpful AI chatbot called 'Exemplar'. "
            "You are very excited about today's hackathon and you should be encouraging and thoughtful in your "
            "responses. People of many different disciplines from Aurecon, an engineering consultancy, will have "
            "approximately 8 hours to come up with an idea for an app and build a prototype."
        )
    )

    def __init__(self, azure_endpoint: str, api_key: str, api_version: str, deployment: str):
        self._messages = Messages([self.SYSTEM_MESSAGE])
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        self.deployment = deployment

    @property
    def messages(self):
        """return only messages that are the assistant and the user"""
        return Messages([msg for msg in self._messages if msg.role is not Role.system])

    def user(self, message: str) -> None:
        """Add a user message"""
        self._messages.append(Message(
            role=Role.user,
            content=message
        ))

    def assistant(self, message: str) -> None:
        """Add an assistant message"""
        self._messages.append(Message(
            role=Role.assistant,
            content=message
        ))

    def get_response(self) -> str:
        """get a message from the agent"""
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=self._messages.format()
        )

        return response.choices[0].message.content

    def stream_response(self):
        """stream a message from the agent"""
        return self.client.chat.completions.create(
            model=self.deployment,
            messages=self._messages.format(),
            stream=True
        )
