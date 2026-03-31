import streamlit as st

from src.models.base import Progress
from src.models.symbols import Symbols
from src.ui.components.pagebase import PageBase


class SettingPage(PageBase):

    @property
    def key(self):
        return "setting"

    @property
    def icon(self):
        return Symbols.setting

    @property
    def title(self):
        return "設定"

    @property
    def title_for_tag(self):
        return "設定"

    def describe(self):
        super().describe()

        st.set_page_config(
            page_title="【無機コレクト】設定変更",
            page_icon=self.icon.value,
        )

        st.title("ストーリーの進行度合い")

        def on_radio_select():
            self.config.set_progress(
                Progress.from_str(st.session_state.get("progress_select"))
            )

        with st.expander("※ストーリーのネタバレを含みます"):
            initial_str = st.session_state.get("progress_select")
            initial_index = Progress.from_str(initial_str) if initial_str else None
            st.radio(
                "progress",
                [p.label for p in list(Progress)],
                label_visibility="collapsed",
                index=initial_index,
                key="progress_select",
                on_change=on_radio_select,
            )
