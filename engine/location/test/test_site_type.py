import pytest
from engine.location.site_type import TSiteType

class TestTSiteType:
    def test_init_defaults(self):
        st = TSiteType('type1', {})
        assert st.pid == 'type1'
        assert st.name == 'type1'
        assert st.pedia == ''
        assert st.marker == 'site'
        assert st.size == 1
        assert st.map_blocks == {}
        assert st.deployment is None

    def test_init_with_data(self):
        data = {'name': 'Terror Site', 'pedia': 'desc', 'marker': 'terror', 'size': 3, 'map_blocks': {'a': 1}, 'deployment': 'aliens'}
        st = TSiteType('type2', data)
        assert st.name == 'Terror Site'
        assert st.pedia == 'desc'
        assert st.marker == 'terror'
        assert st.size == 3
        assert st.map_blocks == {'a': 1}
        assert st.deployment == 'aliens'

