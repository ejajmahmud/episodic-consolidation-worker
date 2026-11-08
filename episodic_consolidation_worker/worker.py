"""Core Episodic Consolidation Worker implementation."""
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Any


class Experience:
    def __init__(self, trigger: str, action: str, success: bool):
        self.trigger = trigger
        self.action = action
        self.success = success


class DeclarativeSchema:
    def __init__(self, trigger: str, recommended_action: str, confidence: float, support_count: int):
        self.trigger = trigger
        self.recommended_action = recommended_action
        self.confidence = confidence
        self.support_count = support_count


class EpisodicConsolidationWorker:
    def __init__(self, min_support: int = 2, min_confidence: float = 0.6):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.experiences: List[Experience] = []
        self.schemas: Dict[str, DeclarativeSchema] = {}

    def record_experience(self, trigger: str, action: str, success: bool):
        self.experiences.append(Experience(trigger, action, success))

    def consolidate(self) -> List[DeclarativeSchema]:
        stats: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(lambda: {"success": 0, "total": 0})
        for exp in self.experiences:
            key = (exp.trigger, exp.action)
            stats[key]["total"] += 1
            if exp.success:
                stats[key]["success"] += 1

        new_schemas = []
        for (trig, act), cnt in stats.items():
            if cnt["total"] >= self.min_support:
                conf = cnt["success"] / float(cnt["total"])
                if conf >= self.min_confidence:
                    schema = DeclarativeSchema(trig, act, conf, cnt["total"])
                    self.schemas[trig] = schema
                    new_schemas.append(schema)
        return new_schemas

    def query_schema(self, trigger: str) -> Optional[DeclarativeSchema]:
        return self.schemas.get(trigger)
