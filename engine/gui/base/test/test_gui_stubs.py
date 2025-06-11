import pytest
from gui.gui_core import TGuiCoreScreen
from engine.gui.base.gui_academy import TGuiAcademy
from engine.gui.base.gui_archive import TGuiArchive
from engine.gui.base.gui_base_info import TGuiBaseInfo
from engine.gui.base.gui_facility import TGuiFacility
from engine.gui.base.gui_hangar import TGuiHangar
from engine.gui.base.gui_lab import TGuiLab
from engine.gui.base.gui_market import TGuiMarket
from engine.gui.base.gui_prison import TGuiPrison
from engine.gui.base.gui_storage import TGuiStorage
from engine.gui.base.gui_transfer import TGuiTransfer
from engine.gui.base.gui_workshop import TGuiWorkshop

@pytest.mark.parametrize("cls", [
    TGuiAcademy, TGuiArchive, TGuiBaseInfo, TGuiFacility, TGuiHangar, TGuiLab,
    TGuiMarket, TGuiPrison, TGuiStorage, TGuiTransfer, TGuiWorkshop
])
def test_stub_gui_instantiation(cls):
    instance = cls()
    assert isinstance(instance, TGuiCoreScreen)

