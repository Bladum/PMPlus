import pytest
from engine.engine.stats import TStatistics

def test_statistics_init():
    stats = TStatistics()
    assert isinstance(stats, TStatistics)
    assert stats.kills == 0
    assert stats.missions_completed == 0
    assert stats.missions_failed == 0
    assert stats.achievements == []

def test_record_kill():
    stats = TStatistics()
    stats.record_kill('unit1')
    assert stats.kills == 1

def test_record_mission_result():
    stats = TStatistics()
    stats.record_mission_result(True)
    assert stats.missions_completed == 1
    stats.record_mission_result(False)
    assert stats.missions_failed == 1

def test_add_achievement():
    stats = TStatistics()
    stats.add_achievement('First Blood')
    assert 'First Blood' in stats.achievements

def test_get_summary():
    stats = TStatistics()
    stats.record_kill('unit1')
    stats.record_mission_result(True)
    stats.add_achievement('First Blood')
    summary = stats.get_summary()
    assert summary['kills'] == 1
    assert summary['missions_completed'] == 1
    assert 'First Blood' in summary['achievements']

