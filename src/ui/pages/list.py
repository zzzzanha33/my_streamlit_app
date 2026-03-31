from typing import List

import streamlit as st

from src.models.base import XRepository as REPO
from src.models.base_for_view import Xshow
from src.models.symbols import Symbols
from src.logic.convert_detail_info import name_for_show
from src.ui.components.config import UserConfig
from src.ui.components.pagebase import PageBase


class ListPage(PageBase):
    def __init__(self, config: UserConfig, repo: REPO, list_xs: List[Xshow]):
        super().__init__(config)
        self.repo = repo
        self.list_xs = list_xs

    @property
    def key(self):
        return "list"

    @property
    def title(self):
        return "一覧"

    @property
    def title_for_tag(self):
        return "合成ルート一覧"

    @property
    def icon(self):
        return Symbols.map

    def describe(self):
        super().describe()

        st.title("一覧")

        for xs in self.list_xs:
            self.show_root(xs)

    def show_root(self, xs: Xshow, is_outside: bool = True):
        name_show = name_for_show(xs)
        if not xs.connect:
            if is_outside:
                with st.expander(f"{name_show}（捕集可能）"):
                    st.page_link(
                        self.pages_dict[xs.name], icon=Symbols.info.value, label="詳細"
                    )

            else:
                st.write(name_show)
        else:
            with st.expander(name_show):
                if is_outside:
                    st.page_link(
                        self.pages_dict[xs.name], icon=Symbols.info.value, label="詳細"
                    )
                if xs.synthesis.catalyst:
                    st.write(Symbols.catalyst.value + xs.synthesis.catalyst.label)
                for ys in xs.connect:
                    self.show_root(ys, False)
