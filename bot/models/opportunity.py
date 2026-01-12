from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class Opportunity:
    name: str
    tags: List[str] 
    deadline: str
    link: Optional[str]= None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            name = data.get("name", "Unnamed"),
            tags=data.get("tags", []),
            deadline= data.get("deadline", ""),
            link = data.get("link", ""),
            description = data.get("description"),
        )
        
    def to_notion(self):
        props= {
            "Name": { "title": [{"text":{"content":self.name}}]},
            "Tags": {"multi_select": [{"name": tag} for tag in self.tags]},
            "Deadline": {"date": {"start": self.deadline}},
        }
        
        if self.link:
            props["Link"] = {"url": self.link}

        # La propiedad Description se comenta porque no existe en la DB de Notion
        # if self.description:
        #     props["Description"] = {"rich_text": [{"text": {"content": self.description}}]}

        return props
