import json
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Input, Label
from textual import on
from datetime import date
from pathlib import Path

TASKS_FILE = Path("tasks.json")

LIST_TASKS = []   # nur noch die Daten, Header merken wir uns anders
COLUMNS = ("task_id", "Task Name", "status", "priority", "subject", "Created at")


def load_tasks():
    global LIST_TASKS
    if TASKS_FILE.exists():
        with TASKS_FILE.open("r", encoding="utf-8") as f:
            LIST_TASKS = json.load(f)
    else:
        LIST_TASKS = []

class TableApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Input(placeholder="Format: Name/status/priority/subject")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*COLUMNS)
        table.add_rows(LIST_TASKS)

    @on(Input.Submitted)
    def add_new_task(self, event: Input.Submitted) -> None:
        inp = event.input              # das Input-Widget
        new_task = inp.value.strip()        # Text aus dem Input

        task_name, status, priority, subject = new_task.split(",")
        
        table = self.query_one(DataTable)

        # einfache ID: nächste Zeilennummer (außer Header)
        next_id = len(table.rows)+1    
        today_str = date.today().strftime("%d.%m.%y")

        # Jetzt wirklich 6 Werte übergeben:
        table.add_row(
            next_id,           
            task_name.strip(),   
            status.strip(),    
            priority.strip(),
            subject.strip(),
            today_str,         
        )

        # Optional auch in LIST_TASKS nachziehen, falls du das noch benutzt:
        LIST_TASKS.append(
            (next_id, task_name, status, priority, subject, today_str)
        )

        with TASKS_FILE.open("w", encoding="utf-8") as file:
            json.dump(LIST_TASKS, file, ensure_ascii=False, indent=2)

        inp.value = ""  # Input-Feld leeren                 


app = TableApp()

if __name__ == "__main__":
    load_tasks()
    app.run()