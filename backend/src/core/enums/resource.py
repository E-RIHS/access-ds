from enum import Enum

class Resource(str, Enum):
    ACTOR = "Actor"
    DOCUMENT = "Document"
    EQUIPMENT = "Equipment"
    EXAMINATION = "Examination"
    METHOD = "Method"
    PROJECT = "Project"
    SERVICE = "Service"
    TECHNIQUE = "Technique"
    TOOL = "Tool"