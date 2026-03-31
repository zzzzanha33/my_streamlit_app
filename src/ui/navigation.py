import streamlit as st

from src.models.base import XRepository as REPO

from src.logic.service import arrange_list_xs

from src.ui.components.config import UserConfig
from src.ui.pages.home import HomePage
from src.ui.pages.list import ListPage
from src.ui.pages.detail import DetailPage
from src.ui.pages.settings import SettingPage


class Router:
    def __init__(self, repo: REPO):
        self.repo = repo
        self.userconfig = UserConfig.get()

        self.list_xs = arrange_list_xs(repo, self.userconfig.progress)

        self.detail_pages = [
            DetailPage(self.userconfig, repo, xs) for xs in self.list_xs
        ]
        self.list_page = ListPage(self.userconfig, repo, self.list_xs)
        self.home_page = HomePage(self.userconfig, self.list_xs)
        self.setting_page = SettingPage(self.userconfig)

        self.pages_dict = self.register_pages()
        self.set_pages_dict()

        self.page = st.navigation(
            {
                "ホーム": [
                    self.pages_dict["home"],
                    self.pages_dict["list"],
                    self.pages_dict["setting"],
                ],
                "各ルート": [self.pages_dict[xs.name] for xs in self.list_xs],
            }
        )

    def register_pages(self):
        pages_dict = {}

        pages_dict[self.home_page.key] = self.home_page.to_streamlit_page
        pages_dict[self.list_page.key] = self.list_page.to_streamlit_page
        pages_dict[self.setting_page.key] = self.setting_page.to_streamlit_page
        for detail_page in self.detail_pages:
            pages_dict[detail_page.key] = detail_page.to_streamlit_page

        return pages_dict

    def set_pages_dict(self):
        self.home_page.set_page_dict(self.pages_dict)
        self.list_page.set_page_dict(self.pages_dict)
        self.setting_page.set_page_dict(self.pages_dict)
        for detail_page in self.detail_pages:
            detail_page.set_page_dict(self.pages_dict)

    def run(self):
        self.page.run()
