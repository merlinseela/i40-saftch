# Standard Imports
from pathlib import Path
# Third Party Imports
# Local Imports

class AasTemplates:
    # Subklassen
    class BoardStatusValues:
        BOOTING = "provisioned"
        IDLE = "ready"
        FLASHING = "occupied"
        TESTING = "offline"

    class TestStatusValues:
        NOTTESTED = "not tested"
        RUNNING = "running"
        TESTED = "tested"
    
    def __init__(self):
        self._path_templates_dir = (Path(__file__).resolve().parent.parent) / "aasx_templates"
        
        # IDTA 02006-3-0-1_Template_Digital Nameplate
        self._aasx_nameplate = "idta_02006_3_0_1_template_digital_nameplate.aasx"
        self._aasx_nameplate_prebaked = "idta_02006_3_0_1_template_digital_nameplate_prebaked.aasx"
        self._nameplate_id = "https://admin-shell.io/idta/SubmodelTemplate/DigitalNameplate/3/0"

        # saftch BoardStatus
        self._aasx_boardstatus = "saftch_template_boardsstatus_prebaked.aasx"
        self._boardstatus_id = "https://example.com/ids/sm/4593_1170_1162_0355"
        self.board_status = self.BoardStatusValues()
        
        # saftch FPGADesign
        self._aasx_fpgadesign = "saftch_template_fpgadesign_prebaked.aasx"
        self._fpgadesign_id = "https://example.com/ids/sm/2200_2170_1162_1095"

        # saftch TestStatus
        self._aasx_teststatus = "saftch_template_teststatus_prebaked.aasx"
        self._teststatus_id = "https://example.com/ids/sm/4472_5170_1162_0073"
        self.test_status = self.TestStatusValues()

    def _get_validated_path(self, filename: str) -> Path:
        absolute_path = self._path_templates_dir / filename
        if not absolute_path.exists():
            raise FileNotFoundError(f"AASX template missing at guaranteed absolute path: {absolute_path}")
        return absolute_path

# GETTER - IDTA 02006-3-0-1_Template_Digital Nameplate
    def get_aasx_nameplate_path(self) -> Path:
        return self._get_validated_path(self._aasx_nameplate)
    def get_aasx_nameplate_prebaked_path(self) -> Path:
        return self._get_validated_path(self._aasx_nameplate_prebaked)
    def get_id_sm_nameplate(self) -> str:
        return self._nameplate_id

# GETTER - saftch BoardStatus
    def get_aasx_boardstatus_path(self) -> Path:
        return self._get_validated_path(self._aasx_boardstatus)
    def get_id_sm_boardstatus(self) -> str:
        return self._boardstatus_id

# GETTER - saftch FPGADesign
    def get_aasx_fpgadesign_path(self) -> Path:
        return self._get_validated_path(self._aasx_fpgadesign)
    def get_id_sm_fpgadessign(self) -> str:
        return self._fpgadesign_id

# GETTER - saftch TestStatus
    def get_aasx_teststatus_path(self) -> Path:
        return self._get_validated_path(self._aasx_teststatus)
    def get_id_sm_teststatus(self) -> str:
        return self._teststatus_id