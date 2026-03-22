import questionary
from models import Task
from storage import TodoStorage

storage = TodoStorage()


def menu():
    """Ana menü döngüsü."""
    while True:
        print()
        choice = questionary.select(
            "Ne yapmak istersin?",
            choices=[
    "📝  Görev ekle",
    "📋  Görevleri listele",
    "✅  Görev tamamla",
    "🗑️   Görev sil",
    "🚪  Çıkış",
],
        ).ask()

        if choice is None:  # Ctrl+C ile çıkış
            break
        elif "ekle" in choice:
            add_task()
        elif "listele" in choice:
            list_tasks()
        elif "sil" in choice:
            delete_task()
        elif "tamamla" in choice:
            complete_task()
        elif "Çıkış" in choice:
            print("Görüşürüz!")
            break


# ── Görev ekle ────────────────────────────────────────────────────────────────

def add_task():
    print()

    title = questionary.text(
        "Görev başlığı:",
        validate=lambda t: True if t.strip() else "Başlık boş olamaz.",
    ).ask()
    if title is None:
        return

    priority = questionary.select(
        "Öncelik:",
        choices=["low", "medium", "high"],
        default="medium",
    ).ask()
    if priority is None:
        return

    deadline = questionary.text(
        "Son tarih (YYYY-AA-GG) — boş bırakabilirsin:",
    ).ask()
    if deadline is None:
        return

    tags_input = questionary.text(
        "Etiketler (virgülle ayır) — boş bırakabilirsin:",
    ).ask()
    if tags_input is None:
        return
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]

    notes = questionary.text(
        "Notlar — boş bırakabilirsin:",
    ).ask()
    if notes is None:
        return

    task = Task(
        title=title.strip(),
        priority=priority,
        deadline=deadline.strip(),
        tags=tags,
        notes=notes.strip(),
    )
    storage.add(task)
    print(f"\n✓ Görev eklendi  [{task.id}]")


# ── Görevleri listele ─────────────────────────────────────────────────────────

def list_tasks():
    tasks = storage.get_all()
    print()

    if not tasks:
        print("Henüz hiç görev yok.")
        return

    # Sütun başlıkları
    print(f"{'ID':<10} {'D':1} {'ÖNCELİK':<8} {'BAŞLIK':<30} {'SON TARİH':<12} ETİKETLER")
    print("─" * 78)

    for t in tasks:
        done     = "✓" if t.done else "○"
        tags_str = ", ".join(t.tags) if t.tags else "—"
        overdue  = " !" if t.is_overdue() else ""
        print(
            f"{t.id:<10} {done:1} {t.priority.upper():<8} "
            f"{t.title[:29]:<30} {(t.deadline or '—') + overdue:<12} {tags_str}"
        )

    total     = len(tasks)
    completed = sum(1 for t in tasks if t.done)
    print(f"\n{total} görev  |  {completed} tamamlandı  |  {total - completed} bekliyor")


# ── Görev sil ─────────────────────────────────────────────────────────────────

def delete_task():
    tasks = storage.get_all()
    print()

    if not tasks:
        print("Silinecek görev yok.")
        return

    choices = [
        questionary.Choice(title=f"[{t.id}] {t.title}", value=t.id)
        for t in tasks
    ]
    choices.append(questionary.Choice(title="← İptal", value=None))

    task_id = questionary.select(
        "Hangi görevi silmek istersin?",
        choices=choices,
    ).ask()

    if task_id is None:
        return

    task_title = next(t.title for t in tasks if t.id == task_id)
    confirm = questionary.confirm(
        f"'{task_title}' silinsin mi?",
        default=False,
    ).ask()

    if confirm:
        storage.delete(task_id)
        print(f"\n✓ Görev silindi.")
    else:
        print("İptal edildi.")


# ── Giriş noktası ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════╗")
    print("║     Todo CLI  📋     ║")
    print("╚══════════════════════╝")
    menu()

def complete_task():
    tasks = storage.get_all()
    print()

    if not tasks:
        print("Tamamlanacak görev yok.")
        return

    choices = [
        questionary.Choice(title=f"[{t.id}] {t.title}", value=t.id)
        for t in tasks if not t.done
    ]

    if not choices:
        print("Zaten tüm görevler tamamlanmış.")
        return

    choices.append(questionary.Choice(title="← İptal", value=None))

    task_id = questionary.select(
        "Hangi görevi tamamlamak istersin?",
        choices=choices,
    ).ask()

    if task_id is None:
        return

    for t in tasks:   # 🔥 BURASI İÇERİDE OLMALI
        if t.id == task_id:
            t.complete()
            storage.update(t)
            print(f"\n✓ '{t.title}' tamamlandı!")
            return