class Task:
    def  __init__(self, name, action ):
        self.name = name
        self.action = action
        self.status = 'PENDING'
        self.upstream = []

    def dependency(self, task):
        self.upstream.append(task)

    def run(self):
        try:
            self.action()
            self.status = 'SUCCESS'
        except Exception:
            self.status = 'FAILED'

    def is_ready(self):
        for t in self.upstream:
            if t.status != 'SUCCESS':
                return False
        return True



def download_data():
    print("-> Downloading data...")

def clear_data():
    print("-> Clear data...")

def load_to_database():
    print("-> Loading to database!")


task_extract = Task("Extract", download_data)
task_transform = Task("Transform", clear_data)
task_load = Task("Load", load_to_database)


task_transform.dependency(task_extract)
task_load.dependency(task_transform)


print("--- Before Start ---")
print(f"Is {task_transform.name} could go? {task_transform.is_ready()}")


print("\n--- STARTING EXTRACT ---")
task_extract.run()


print("\n--- AFTER RUNNING EXTRACT ---")
print(f"Is {task_transform.name} could go? {task_transform.is_ready()}")
print(f"Is {task_load.name} could go? {task_load.is_ready()}")


class Scheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def run_all(self):
        while True:
            tasks_left = False
            for t in self.tasks:
                if t.status == 'PENDING':
                    tasks_left = True
                    if t.is_ready():
                        t.run()
            if not tasks_left:
                break


def extract(): print("[1] Downloading data from API...")
def transform(): print("[2] Clearing and formating data...")
def load(): print("[3] Loading clear data to SQL!")

t_extract = Task("Extract", extract)
t_transform = Task("Transform", transform)
t_load = Task("Load", load)


t_transform.dependency(t_extract)
t_load.dependency(t_transform)


scheduler = Scheduler()
scheduler.add_task(t_extract)
scheduler.add_task(t_transform)
scheduler.add_task(t_load)


print("--- STARTING PIPELINE ---")
scheduler.run_all()
print("--- END OF WORK, LOADED ---")