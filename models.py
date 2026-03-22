from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, List
import uuid


Priority = Literal["low", "medium", "high"]


@dataclass
class Task:
    title: str
    priority: Priority = "medium"
    deadline: str = ""           # "2025-12-31" formatında ya da boş
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    done: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    # --- Yardımcı metodlar ---

    def complete(self):
        """Görevi tamamlandı olarak işaretle."""
        self.done = True

    def is_overdue(self) -> bool:
        """Deadline geçmiş ve görev bitmemişse True döner."""
        if not self.deadline or self.done:
            return False
        try:
            due = datetime.strptime(self.deadline, "%Y-%m-%d")
            return datetime.now() > due
        except ValueError:
            return False

    def to_dict(self) -> dict:
        """JSON'a kaydetmek için dict'e çevirir."""
        return {
            "id":         self.id,
            "title":      self.title,
            "priority":   self.priority,
            "deadline":   self.deadline,
            "tags":       self.tags,
            "notes":      self.notes,
            "done":       self.done,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """JSON'dan okunan dict'i Task nesnesine çevirir."""
        return cls(
            id=data["id"],
            title=data["title"],
            priority=data.get("priority", "medium"),
            deadline=data.get("deadline", ""),
            tags=data.get("tags", []),
            notes=data.get("notes", ""),
            done=data.get("done", False),
            created_at=data.get("created_at", ""),
        )

    def __str__(self) -> str:
        status = "✓" if self.done else "○"
        tag_str = f"  [{', '.join(self.tags)}]" if self.tags else ""
        due_str = f"  → {self.deadline}" if self.deadline else ""
        return f"[{status}] ({self.priority.upper()}) {self.title}{due_str}{tag_str}"




    
