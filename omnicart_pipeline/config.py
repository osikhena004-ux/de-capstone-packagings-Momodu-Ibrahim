from importlib import resources
import configparser

class Configuration:
    def __init__(self, base_url: str , page_limit: int):
        self.base_url = base_url
        self.page_limit = page_limit

    @classmethod
    def from_package(cls):
        cfg_text = (resources.files("omnicart_pipeline").
                    joinpath("pipeline.cfg").read_text(encoding = "utf-8"))
        cp = configparser.ConfigParser()
        cp.read_string(cfg_text)
        base_url = cp["DEFAULT"].get("base_url")
        page_limit = cp["DEFAULT"].getint("pagination_limit", fallback = 5)
        if not base_url:
            raise ValueError("base_url missing.")
        return cls(base_url, page_limit)