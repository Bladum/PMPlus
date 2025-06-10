import pytest
from engine.engine.modloader import TModLoader
from pathlib import Path
import tempfile
import os
import yaml

def test_modloader_init():
    loader = TModLoader('TestMod', '.')
    assert loader.mod_name == 'TestMod'
    assert isinstance(loader.mod_path, Path)
    assert loader.yaml_data == {}

def test_load_all_yaml_files(tmp_path):
    # Create a fake rules directory with a YAML file
    rules_dir = tmp_path / 'rules'
    rules_dir.mkdir()
    yaml_file = rules_dir / 'test.yaml'
    data = {'facilities': {'base1': {'name': 'Base 1'}}}
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
    loader = TModLoader('TestMod', tmp_path)
    loader.load_all_yaml_files()
    assert 'facilities' in loader.yaml_data
    assert 'base1' in loader.yaml_data['facilities']

def test_load_all_yaml_files_missing_rules(tmp_path):
    loader = TModLoader('TestMod', tmp_path)
    with pytest.raises(FileNotFoundError):
        loader.load_all_yaml_files()

