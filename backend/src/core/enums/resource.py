from enum import Enum

class Resource(str, Enum):
    ACTOR = "Actor"
    EQUIPMENT = "Equipment"
    EXAMINATION = "Examination"
    PROJECT = "Project"
    SERVICE = "Service"
    TECHNIQUE = "Technique"
    TOOL = "Tool"