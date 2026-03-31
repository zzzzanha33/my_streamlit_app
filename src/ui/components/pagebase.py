from abc import ABC, abstractmethod
import streamlit as st

from src.models.symbols import Symbols
from src.ui.components.config import UserConfig


class PageBase(ABC):
    def __init__(self, config: UserConfig):
        self.pages_dict = {}
        self.config = config

    @property
    @abstractmethod
    def key(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def title_for_tag(self):
        pass

    @property
    @abstractmethod
    def icon(self) -> Symbols:
        pass

    @property
    def url_path(self) -> str:
        return self.title.lower().replace(" ", "-")

    @property
    def to_streamlit_page(self):
        return st.Page(
            self.run, title=self.title, icon=self.icon.value, url_path=self.url_path
        )

    def run(self):
        self.config.add_key_to_history(self.key)
        self.describe()

    def set_page_dict(self, pages_dict: dict[str]):
        self.pages_dict = pages_dict

    @abstractmethod
    def describe(self):
        with st.container(horizontal=True):
            st.page_link(self.pages_dict["home"])
            st.page_link(self.pages_dict["list"])
            st.page_link(self.pages_dict["setting"])
            for page_key in self.config.history:
                if page_key in self.pages_dict:
                    st.page_link(self.pages_dict[page_key])

        with st.sidebar.container():
            st.write(f"進行度：{self.config.progress.label}")
            st.page_link(self.pages_dict["setting"])
