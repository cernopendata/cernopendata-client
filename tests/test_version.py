"""cernopendata-client version test."""


def test_version():
    """Test version import."""
    from cernopendata_client import __version__
    assert __version__
