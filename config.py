"""
Basic Azure OpenAI config
"""
from dataclasses import dataclass
from pathlib import Path
import tomllib
from typing import Any, Dict

CONFIG_FILENAME = ".config.toml"
CONFIG_PATH = Path().cwd() / CONFIG_FILENAME
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)

# Default to an empty dict if no openai config is found
openai_vars: Dict[str, Any] = config.get("openai", {})

@dataclass
class openai:
    """
    OpenAI related config variables
    
    Parameters:
    -----------
    - API_TYPE: str, should be set to `azure` for current version of Bamboo
    - API_VERSION: str, the OpenAI API version 
    - API_BASE: str, the API endpoint base
    - API_KEY: str, the API key
    - DEPLOYMENT_NAME: str, the name of the Azure Deployment for the chatgpt instance
    """
    API_TYPE: str = openai_vars.get("API_TYPE", "azure")
    API_VERSION: str = openai_vars.get("API_VERSION", "2023-12-01-preview")
    API_BASE: str = openai_vars.get("API_BASE")
    API_KEY: str = openai_vars.get("API_KEY")
    DEPLOYMENT_NAME: str = openai_vars.get("DEPLOYMENT_NAME")
