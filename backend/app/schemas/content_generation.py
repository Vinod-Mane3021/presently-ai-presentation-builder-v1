from typing import Literal, Optional

PresentationType = Literal[
    "pitch_deck", "sales_deck", "report", "training",
    "lecture", "marketing", "internal_update",
    "investor_deck", "other"
]

GoalType = Literal[
    "inform", "persuade", "sell", "update",
    "train", "raise_funds", "onboard", "other"
]


ToneType = Literal[
    "formal", "informal", "storytelling", "data_driven",
    "inspirational", "playful", "technical", "neutral"
]

AspectRatio = Literal["16:9", "4:3", "9:16"]

ExportFormat = Literal["pptx", "pdf", "google_slides", "images_zip"]

ImageSource = Literal["ai_generated", "stock", "user_uploaded", "mixed"]

ImageDensity = Literal["low", "medium", "high"]

SpeakerNotesStyle = Literal["bullet_points", "script_like"]

SpeakerNotesLength = Literal["short", "detailed"]

VisualStyle = Literal[
    "minimal", "corporate", "playful", "creative", "dark", "light"
]

ComplianceMode = Literal["none", "finance", "healthcare"]

TargetAudience = Literal["executives", "students", "investors", "customers"]

AudienceBackground = Literal["tech", "non-tech"]

class GeneratePresentationRequest:
    prompt: str
    user_id: str
    presentation_type: PresentationType
    target_audience: TargetAudience
    audience_background: AudienceBackground
    goal: GoalType
    num_slides: Optional[int] = 12
    language: Optional[str] = "en"
    tone: Optional[ToneType] = "neutral"

class GenerateOutlineResponse:
    title: str
    outlines: list[str]

class Slide:
    id: str
    title: str
    points: list[str]
    image_required: bool
    image_gen_prompt: str
    image_url: str

class PresentationResponse:
    title: str
    description: str
    slides: list[Slide] 




