from functools import partial
import streamlit as st
import pandas as pd

from structure_for_synthesis import XRepository as REPO
from interface import (
    arrange,
    count_needed,
    describe_process,
    build_mermaid_text,
    build_all_tree,
    Xshow,
)


class UI:
    def __init__(self, repo: REPO):
        self.repo = repo
        self.list_xs = arrange(self.repo)

        self.home_page = st.Page(
            self.page_home, title="HOME", icon="🏠", url_path="home"
        )

        self.detail_pages = {
            xs.name: st.Page(
                partial(self.page_detail, xs=xs),
                title=xs.name,
                icon="🌼" if xs.is_special else "🌱",
                url_path=xs.name,
            )
            for xs in self.list_xs
        }

        self.alltree_page = st.Page(
            self.page_all, title="全部盛り", icon="🗾", url_path="alltree"
        )

        self.page = st.navigation(
            {"ホーム": [self.home_page], "各ルート": list(self.detail_pages.values())}
        )

    def page_detail(self, xs: Xshow):
        ingredients = count_needed(xs, {})
        processes = describe_process(xs)
        mm_code = build_mermaid_text(xs)

        st.title(f"{xs.name}の作り方（詳細）")

        st.header("材料")

        df = pd.DataFrame(
            {
                "名前": [ys.name for ys in ingredients],
                "数": [ingredients[ys] for ys in ingredients],
            }
        )

        st.write(df)

        st.header("手順")

        for i, ys in enumerate(processes):
            text_catalyst = f"⏳{ys.catalyst}で" if ys.catalyst else ""
            text = f"{i+1}. {"と".join([("🌼" if zs.is_special else "🌱")+zs.name for zs in ys.connect])}を{text_catalyst}合成し、{("🌼" if ys.is_special else "🌱")+ys.name}を作る。"
            st.write(text)

        st.header("図")

        st.graphviz_chart(mm_code, width="stretch")

        if st.button("戻る"):
            st.switch_page(self.home_page)

    def show_root(self, xs: Xshow, text: str):
        if not xs.connect:
            st.write(f"{"🌼" if xs.is_special else "🌱"} {xs.name}")
        else:
            with st.expander(
                f"{"🌼" if xs.is_special else "🌱"} {xs.name}  (rank:{xs.rank} , effort:{xs.effort})",
                key=f"expander_{text+xs.name}",
            ):
                if not text:
                    if st.button("詳細", key=f"btn{xs.name}"):
                        st.switch_page(
                            self.detail_pages[xs.name],
                        )
                if xs.catalyst:
                    st.write(f"⏳{xs.catalyst}")
                for ys in xs.connect:
                    self.show_root(ys, text + xs.name)

    def page_home(self):

        st.title("一覧")

        for xs in self.list_xs:
            self.show_root(xs, "")

    def page_all(self):
        code = build_all_tree(self.list_xs)
        st.title("全体図")

        st.graphviz_chart(code)

    def run(self):
        self.page.run()
