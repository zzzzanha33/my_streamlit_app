from functools import partial
import streamlit as st
import pandas as pd

from structure_for_synthesis import XRepository as REPO
from interface import (
    arrange,
    count_needed,
    describe_process,
    build_mermaid_text,
    search_children,
    Xshow,
)


class UI:
    def __init__(self, repo: REPO):
        self.repo = repo
        self.list_xs = arrange(self.repo)

        self.home_page = st.Page(
            self.page_home, title="ホーム", icon="🏠", url_path="home"
        )

        self.list_page = st.Page(
            self.page_list, title="一覧", icon="🗺️", url_path="list"
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

        self.page = st.navigation(
            {
                "ホーム": [self.home_page, self.list_page],
                "各ルート": list(self.detail_pages.values()),
            }
        )

    def page_detail(self, xs: Xshow):
        ingredients = count_needed(xs, {})
        processes = describe_process(xs)
        mm_code = build_mermaid_text(xs)
        list_children = search_children(xs, xs, [])

        st.set_page_config(
            page_title=f"【無機コレクト】{xs.name}の合成手順",
            page_icon="🌼" if xs.is_special else "🌱",
        )

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

        if list_children != []:
            st.header("関連項目")
            with st.container(horizontal=True):
                for ys in list_children:
                    if st.button(ys.name, key=f"btn{xs.name}-{ys.name}"):
                        st.switch_page(self.detail_pages[ys.name])

        st.write("")

        with st.container(horizontal=True):
            if st.button("一覧に戻る"):
                st.switch_page(self.list_page)
            if st.button("ホームに戻る"):
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
                        st.switch_page(self.detail_pages[xs.name])
                if xs.catalyst:
                    st.write(f"⏳{xs.catalyst}")
                for ys in xs.connect:
                    self.show_root(ys, text + xs.name)

    def page_list(self):
        st.set_page_config(page_title="【無機コレクト】合成ルート一覧", page_icon="🗺️")

        st.title("一覧")

        for xs in self.list_xs:
            self.show_root(xs, "")

    def page_home(self):
        st.set_page_config(
            page_title="【無機コレクト】合成ルートまとめ/ホーム", page_icon="🧪"
        )

        st.title("ホーム")

        st.header("概要")
        content_text = """
        無機コレクトの、特に合成というシステムに着目して、あるモンスターを合成するために必要な手順等をまとめました。\n
        なるべく少ない工程でできるように試していますが、素人ゆえ、間違いやバグがあるかもしれません。使えそうだと思ったらお使いください。\n
        """
        st.write(content_text)

        if st.button("生成物一覧へ"):
            st.switch_page(self.list_page)

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
            if st.button(selected, f"search_btn{selected}"):
                st.switch_page(self.detail_pages[selected])

    def run(self):
        self.page.run()
