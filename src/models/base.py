"""合成用の構造"""

from enum import IntEnum
from typing import List, Iterator


class Progress(IntEnum):
    mendere_mura = 0
    mendere_suigen = 1
    osuto_mura = 2
    osuto_mori = 3
    harbor = 4
    bosh = 5
    sorube_yama = 6
    sorube_mura = 7
    hesu_sabaku = 8
    hesu_oasis = 9
    sharuru_yougan = 10
    sharuru_shuuraku = 11
    mendere_chika = 12
    abogado = 13
    innseki = 14
    story_clear = 15

    @property
    def label(self):
        names = {
            Progress.mendere_mura: "メンデレ村",
            Progress.mendere_suigen: "メンデレ水源",
            Progress.osuto_mura: "オストワルトの村",
            Progress.osuto_mori: "オストワルトの森",
            Progress.harbor: "港町ハーバー",
            Progress.bosh: "ボッシュ洞窟",
            Progress.sorube_yama: "ソルベ雪山",
            Progress.sorube_mura: "ソルベ村",
            Progress.hesu_sabaku: "ヘス砂漠",
            Progress.hesu_oasis: "ヘスのオアシス",
            Progress.sharuru_yougan: "シャルル溶岩地帯",
            Progress.sharuru_shuuraku: "シャルルの集落",
            Progress.mendere_chika: "メンデレ村地下",
            Progress.abogado: "アボガド遺跡",
            Progress.innseki: "隕石落下地点",
            Progress.story_clear: "ストーリークリア後",
        }
        return names[self]

    @staticmethod
    def from_str(text: str):
        names = {
            Progress.mendere_mura: "メンデレ村",
            Progress.mendere_suigen: "メンデレ水源",
            Progress.osuto_mura: "オストワルトの村",
            Progress.osuto_mori: "オストワルトの森",
            Progress.harbor: "港町ハーバー",
            Progress.bosh: "ボッシュ洞窟",
            Progress.sorube_yama: "ソルベ雪山",
            Progress.sorube_mura: "ソルベ村",
            Progress.hesu_sabaku: "ヘス砂漠",
            Progress.hesu_oasis: "ヘスのオアシス",
            Progress.sharuru_yougan: "シャルル溶岩地帯",
            Progress.sharuru_shuuraku: "シャルルの集落",
            Progress.mendere_chika: "メンデレ村地下",
            Progress.abogado: "アボガド遺跡",
            Progress.innseki: "隕石落下地点",
            Progress.story_clear: "ストーリークリア後",
        }
        for progress in names:
            if progress.label == text:
                return progress
        return Progress.story_clear


class X:
    def __init__(
        self,
        name: str,
        repo: "XRepository",
        habitat: Progress = None,
        synthesises: List["Synthesis"] = None,
        is_valid=False,
    ):
        self.name = name
        if habitat is None:
            habitat = Progress.story_clear
        self.habitat = habitat
        if synthesises is None:
            synthesises = []
        self.synthesises = synthesises
        self._repo = repo
        self.is_valid = is_valid

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, X):
            return False
        return self.name == other.name


class Catalyst(IntEnum):
    heat = 1
    press = 2
    he_pre = 3
    elec = 4
    harbor = 5
    pt = 6
    mno2 = 7
    fe3o4 = 8
    v2o5 = 9

    @property
    def progress(self) -> Progress:
        progresses = {
            Catalyst.heat: Progress.harbor,
            Catalyst.press: Progress.harbor,
            Catalyst.he_pre: Progress.story_clear,
            Catalyst.elec: Progress.hesu_oasis,
            Catalyst.harbor: Progress.abogado,
            Catalyst.pt: Progress.story_clear,
            Catalyst.mno2: Progress.bosh,
            Catalyst.fe3o4: Progress.abogado,
            Catalyst.v2o5: Progress.abogado,
        }
        return progresses[self]

    @property
    def label(self):
        names = {
            Catalyst.heat: "高温の素",
            Catalyst.press: "高圧の素",
            Catalyst.he_pre: "高温高圧の素",
            Catalyst.elec: "電気の素",
            Catalyst.harbor: "ハーバー・ボッシュ",
            Catalyst.pt: "Pt触媒",
            Catalyst.mno2: "MnO2触媒",
            Catalyst.fe3o4: "四酸化三鉄触媒",
            Catalyst.v2o5: "V2O5触媒",
        }
        return names[self]

    @staticmethod
    def from_str(text: str):
        names = {
            Catalyst.heat: "高温の素",
            Catalyst.press: "高圧の素",
            Catalyst.he_pre: "高温高圧の素",
            Catalyst.elec: "電気の素",
            Catalyst.harbor: "ハーバー・ボッシュ",
            Catalyst.pt: "Pt触媒",
            Catalyst.mno2: "MnO2触媒",
            Catalyst.fe3o4: "四酸化三鉄触媒",
            Catalyst.v2o5: "V2O5触媒",
        }
        for catalyst in names:
            if catalyst.label == text:
                return catalyst
        return None

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if not isinstance(other, Catalyst):
            return False
        return self.value == other.value


class Synthesis:
    def __init__(self, y: X, catalyst: Catalyst, *x: X):

        self.y = y
        self.catalyst = catalyst
        self.x = list(x)

    def text_for_print(self):
        if self == None:
            return "まだなし。"
        else:
            return "+".join([x.name for x in self.x]) + "->" + self.y.name

    def is_native(self):
        return not self.x

    def __eq__(self, other):
        if not isinstance(other, Synthesis):
            return False
        return (
            (self.y == other.y)
            and (self.catalyst == other.catalyst)
            and (self.x == other.x)
        )

    def is_valid(self, progress: Progress):
        catalyst_ok = (self.catalyst is None) or (self.catalyst.progress <= progress)
        return catalyst_ok and (self.y.is_valid) and all(x.is_valid for x in self.x)

    def is_ready(self, progress: Progress):
        if self.is_native():
            return self.y.habitat <= progress
        else:
            x_ok = all(x.is_valid for x in self.x)
            catalyst_ok = (self.catalyst is None) or (
                self.catalyst.progress <= progress
            )
            return x_ok and catalyst_ok


class XRepository:
    def __init__(self):
        self._storage: dict[str, X] = {}

    def register_x(self, name: str):
        if not self.exists(name):
            self._storage[name] = X(name, self)
        return self

    def register_synthesis(self, synthesis: Synthesis):
        self._storage[synthesis.y.name].synthesises.append(synthesis)
        return self

    def register_habitat(self, x_name: str, habitat: Progress):
        self._storage[x_name].habitat = habitat
        return self

    def __getitem__(self, name: str) -> "X":
        return self._storage[name]

    def exists(self, name: str) -> bool:
        return name in self._storage

    def all(self):
        return [(key, self._storage[key]) for key in list(self._storage)]

    def __iter__(self) -> Iterator["X"]:
        return iter(self._storage.values())

    def __len__(self):
        return len(self._storage)
