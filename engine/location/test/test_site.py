import pytest
from engine.location.site import TSite
from unittest.mock import MagicMock

class TestTSite:
    def test_init_sets_attributes(self, monkeypatch):
        mock_game = MagicMock()
        mock_game.mod.sites.get.return_value = 'site_type_obj'
        monkeypatch.setattr('engine.engine.game.TGame', lambda: mock_game)
        data = {'site_type': 'alien_base'}
        site = TSite('site1', data)
        assert site.site_type == 'site_type_obj'
        assert isinstance(site.map_blocks, dict)

    def test_generate_random_map_blocks(self, monkeypatch):
        monkeypatch.setattr('random.choice', lambda l: l[0])
        site = TSite('site2', {'site_type': 'type'})
        blocks = site.generate_random_map_blocks(2)
        assert list(blocks.keys()) == ['block_1', 'block_2']
        assert all(v in ['urban', 'forest', 'farm', 'desert', 'mountain'] for v in blocks.values())

