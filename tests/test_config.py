from omnicart_pipeline.config import Configuration

def test_config_from_package():
    cfg = Configuration.from_package()
    assert cfg.base_url.startswith("http")
    assert isinstance(cfg.pagination_limit, int)
