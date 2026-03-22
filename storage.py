import json
import os
from models import Task


class TodoStorage:
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath

    def load(self) -> list[Task]:
        """JSON dosyasından görevleri okur. Dosya yoksa boş liste döner."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task.from_dict(item) for item in data]

    def save(self, tasks: list[Task]) -> None:
        """Görev listesini JSON dosyasına yazar."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)

    def get_all(self) -> list[Task]:
        """Tüm görevleri döndürür."""
        return self.load()

    def add(self, task: Task) -> None:
        """Yeni görevi ekler ve kaydeder."""
        tasks = self.load()
        tasks.append(task)
        self.save(tasks)

    def delete(self, task_id: str) -> bool:
        """Verilen id'ye sahip görevi siler. Başarılıysa True döner."""
        tasks = self.load()
        filtered = [t for t in tasks if t.id != task_id]

        if len(filtered) == len(tasks):
            return False  # Görev bulunamadı

        self.save(filtered)
        return True

    def update(self, updated_task: Task) -> bool:
        """Var olan bir görevi günceller. Başarılıysa True döner."""
        tasks = self.load()
        for i, task in enumerate(tasks):
            if task.id == updated_task.id:
                tasks[i] = updated_task
                self.save(tasks)
                return True
        return False  # Görev bulunamadı


# --- Basit kullanım örneği ---
if __name__ == "__main__":
    storage = TodoStorage("test_tasks.json")

    # Görev ekle
    storage.add(Task(title="storage.py yaz", priority="high", tags=["backend"]))
    storage.add(Task(title="ui.py yaz",      priority="medium", deadline="2025-09-01"))
    storage.add(Task(title="README yaz",     priority="low"))

    # Listele
    tasks = storage.get_all()
    print(f"{len(tasks)} görev yüklendi:\n")
    for t in tasks:
        print(" ", t)

    # Güncelle
    tasks[0].complete()
    storage.update(tasks[0])
    print(f"\n'{tasks[0].title}' tamamlandı olarak işaretlendi.")

    # Sil
    storage.delete(tasks[2].id)
    print(f"'{tasks[2].title}' silindi.")

    print(f"\nKalan görevler: {len(storage.get_all())}")

    # Test dosyasını temizle
    os.remove("test_tasks.json")