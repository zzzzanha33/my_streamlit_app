from typing import List

import streamlit as st

from src.models.base import Progress


class UserConfig:
    SESSION_KEY = "userconfig"

    HISTORY_LIMIT = 5

    def __init__(self):
        self.history: List[str] = []
        self.progress = Progress.story_clear

    @classmethod
    def get(cls) -> "UserConfig":
        if cls.SESSION_KEY not in st.session_state:
            st.session_state[cls.SESSION_KEY] = cls()
        return st.session_state[cls.SESSION_KEY]

    def add_key_to_history(self, page_key: str):
        length = len(self.history)
        if page_key in ["home", "list", "setting"]:
            return
        elif page_key in self.history:
            self.history = [key for key in self.history if key != page_key]
            self.history.append(page_key)
        elif length >= self.HISTORY_LIMIT:
            margin = length - self.HISTORY_LIMIT
            self.history = [self.history[i] for i in range(length) if i > margin]
            self.history.append(page_key)
        else:
            self.history.append(page_key)

    def set_progress(self, progress: Progress):
        self.progress = progress
