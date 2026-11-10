"""
Context Board to share information across the SSOT.
"""
# Standard Imports
# Third Party Imports
from dotenv import dotenv_values
# Local Imports
from core.aas_templates import AasTemplates
from utils.basyxclient import BasyxAPIClient

class SSOTContext:
    """
    Custom Data Class to house and share information across the SSOT.
    """
    def __init__(self):
        # Bootstrapping Environment Values and Core/Utility Classes
        self.ssot_environment: dict = dotenv_values(".env")
        self.basyxclient: BasyxAPIClient = BasyxAPIClient(self.ssot_environment['BASYX_AAS_ENVIRONMENT'])
        self.aas_templates: AasTemplates = AasTemplates()