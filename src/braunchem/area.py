from braunchem.topic import TopicSet

from pydantic import BaseModel


class Area(BaseModel):
    """Area (Química Inorgânica, Orgânica, Analítica, Físico-Química)"""

    id_: str
    title: str
    topic_set: TopicSet

    def parse_json():
        return


class AreaSet(BaseModel):
    """Conjunto de areas"""

    def parse_json():
        return
