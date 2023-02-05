from enum import Enum

class Resource(str, Enum):
    EXAMINATION = "Examination"
    SERVICE = "Service"
    PROJECT = "Project"