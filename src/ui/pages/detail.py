import streamlit as st
import pandas as pd

from src.models.base import XRepository as REPO
from src.models.base_for_view import Xshow
from src.logic.convert_detail_info import (
    count_needed,
    describe_process,
    build_mermaid_text,
    search_children,
    decide_icon_for_page,
    name_for_show,
)
from src.models.symbols import Symbols
from src.ui.components.config import UserConfig
from src.ui.components.pagebase import PageBase


class DetailPage(PageBase):
    def __init__(self, config: UserConfig, repo: REPO, xs: Xshow):
        super().__init__(config)
        self.repo = repo
        self.xs = xs

    @property
    def key(self):
        return self.xs.name

    @property
    def icon(self):
        return decide_icon_for_page(self.xs)

    @property
    def title(self):
        return f"{self.xs.name}"

    @property
    def title_for_tag(self):
        return f"{self.xs.name}の作り方(詳細)"

    def describe(self):
        super().describe()

        ingredients = count_needed(self.xs)
        processes = describe_process(self.xs)
        mm_code = build_mermaid_text(self.xs)
        list_children = sorted(
            search_children(self.xs), key=lambda xs: xs.x.habitat, reverse=True
        )

        st.set_page_config(
            page_title=f"【無機コレクト】{self.xs.name}の合成手順",
            page_icon=self.icon.value,
        )

        if self.xs.is_tip:
            st.title(f"{self.xs.name}の捕集")
        else:
            st.title(f"{self.xs.name}の作り方（詳細）")

        if self.xs.is_tip:
            st.header("捕集場所・条件")
        else:
            st.header("材料")
        ingredient_list, num_list, habitat_list = (
            [
                ingredient.name
                for ingredient in sorted(ingredients, key=lambda xs: xs.x.habitat)
            ],
            [
                ingredients[ingredient]
                for ingredient in sorted(ingredients, key=lambda xs: xs.x.habitat)
            ],
            [
                ingredient.x.habitat.label
                for ingredient in sorted(ingredients, key=lambda xs: xs.x.habitat)
            ],
        )
        df = pd.DataFrame(
            {"名前": ingredient_list, "数": num_list, "場所・条件": habitat_list}
        )
        st.write(df)

        if not self.xs.is_tip:
            st.header("手順")

        for i, synthesis in enumerate(processes):
            text_catalyst = (
                f"{Symbols.catalyst.value}{synthesis.catalyst.label}で"
                if synthesis.catalyst
                else ""
            )
            text_ingredient = " と".join([name_for_show(ys) for ys in synthesis.xs])
            text_product = name_for_show(synthesis.ys)
            text = f"{i+1}. {text_ingredient}を{text_catalyst}合成し、{text_product}を作る。"
            st.write(text)

        if not self.xs.is_tip:
            st.header("図")
            st.graphviz_chart(mm_code, width="stretch")

        if list_children != []:
            st.header("関連項目")
            with st.container(horizontal=True):
                for ys in list_children:
                    st.page_link(
                        self.pages_dict[ys.name],
                        label=(ys.name),
                    )

        st.write("")

        with st.container(horizontal=True):
            if st.button("一覧に戻る"):
                st.switch_page(self.pages_dict["list"])
            if st.button("ホームに戻る"):
                st.switch_page(self.pages_dict["home"])
