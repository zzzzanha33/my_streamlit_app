from typing import List

import streamlit as st

from src.models.base_for_view import Xshow
from src.models.symbols import Symbols
from src.ui.components.config import UserConfig
from src.ui.components.pagebase import PageBase


class HomePage(PageBase):

    def __init__(self, config: UserConfig, list_xs: List[Xshow]):
        super().__init__(config)
        self.list_xs = list_xs

    @property
    def key(self):
        return "home"

    @property
    def title(self):
        return "ホーム"

    @property
    def title_for_tag(self):
        return "ホーム"

    @property
    def icon(self):
        return Symbols.home

    def describe(self):
        super().describe()

        st.title("ホーム")

        st.header("概要")
        content_text = """
        無機コレクトの、特に合成というシステムに着目して、あるモンスターを合成するために必要な手順等をまとめました。\n
        何が必要で何をすべきか、全体像がよく見えるように心がけています。\n
        なるべく少ない工程でできるように試していますが、素人ゆえ、間違いやバグがあるかもしれません。使えそうだと思ったらお使いください。\n
        ※ストーリークリアしていることを前提にしています。ストーリーの途中なら、下にある設定から進行度を調節し、一覧や各ページをご覧ください。\n
        """
        st.write(content_text)

        if st.button("一覧へ"):
            st.switch_page(self.pages_dict["list"])

        st.header("探す")
        list_xs_name = [xs.name for xs in self.list_xs]
        selected = st.selectbox(
            "合成したいモンスターを探す",
            options=list_xs_name,
            index=None,
            placeholder="ex: 王水,炭酸ナトリウム",
        )
        if selected:
            st.write(f"👉「{selected}」の詳細を確認中")
            st.page_link(self.pages_dict[selected])

        st.header("設定")
        st.page_link(self.pages_dict["setting"])
