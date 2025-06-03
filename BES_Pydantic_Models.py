from pydantic import BaseModel, Field
from enum import Enum

class BeliefPresent(str, Enum):
    true = "true"
    false = "false"

class DetectBelief(BaseModel):
    belief_detected: BeliefPresent
    #confidence_score: ConfidenceScore

class BeliefImpact(str, Enum):
    positive = "positive"
    negative = "negative"

class BeliefDimension(str, Enum):
    personal = "Personal"
    professional = "Professional"
    social = "Social"
    growth = "Growth"

class BeliefCategory(str, Enum):
    self_efficacy = "Self-efficacy statement"
    growth_mindset = "Growth mindset expression"
    self_identity = "Self-identity assertion"
    coping_mechanism = "Coping mechanism beliefs"
    meaning_making = "Meaning-making statements"
    future_oriented = "Future-oriented perception"
    
class ExtractBelief(BaseModel):
    belief: str = Field(description="The extracted self-perception belief")
    impact: BeliefImpact
    dimension: BeliefDimension
    category: BeliefCategory

class ConfidenceScore(str, Enum):
    high = 'high'
    moderate = 'moderate'
    low = 'low'