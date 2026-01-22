import datetime
import time
import logging

# Настроим базовую конфигурацию логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    encoding="utf-8",
    filename='logfile.txt',
    filemode='w'
)

# Дата и время текущего момента (для глобального отслеживания)
date_time_str = None

def logger_time():
    """
    Функция для записи успешного добавления времени выполнения задачи в журнал.
    """
    global date_time_str
    current_time = datetime.datetime.now()
    date_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Успешное добавление времени к задаче: {date_time_str}")

# Файл хранения задач
TASK_FILE = "tasks.txt"

def add_task():
    """
    Добавляет новую задачу в файл задач.
    """
    task = input("Введите задачу: ")
    date_str = input("Введите время выполнения задачи в формате ГГГГ-ММ-ДД: ")

    try:
        # Преобразуем введённую дату в нужный формат
        plan_time = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        logging.error(f"Ошибка: Некорректный формат даты '{date_str}'. Ожидаемый формат: ГГГГ-ММ-ДД.")
        print("Ошибка: неверный формат даты. Должен быть ГГГГ-ММ-ДД.")
        return

    # Сохраняем задачу в файл
    with open(TASK_FILE, mode='a', encoding="utf-8") as file:
        file.write(f"{task}: {plan_time}\n")

    logging.info(f"Задача '{task}' успешно добавлена на {plan_time}")
    print(f"Задача '{task}' успешно запланирована на {plan_time}")

def load_tasks():
    """
    Загружает список задач из файла.
    """
    tasks = []
    try:
        with open(TASK_FILE, mode='r', encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(": ")
                if len(parts) == 2:
                    task, due_date = parts
                    tasks.append((task, due_date))
    except FileNotFoundError:
        logging.warning(f"Файл задач '{TASK_FILE}' не найден.")
        print(f"Внимание: файл задач '{TASK_FILE}' не найден.")
        return []
    return tasks

def show_tasks():
    """
    Отображает список текущих задач.
    """
    tasks = load_tasks()
    if not tasks:
        print("Нет задач.")
    else:
        print("Список задач:")
        for i, (task, due_date) in enumerate(tasks, start=1):
            print(f"{i}. Задача: {task}, Срок исполнения: {due_date}")

def save_tasks(tasks):
    """
    Сохраняет список задач в файл.
    """
    with open(TASK_FILE, mode='w', encoding="utf-8") as file:
        for task, due_date in tasks:
            file.write(f"{task}: {due_date}\n")

def check_and_notify(tasks):
    """
    Проверяет задачи и выводит уведомление, удаляя просроченные задачи.
    """
    today = datetime.datetime.now().date()
    updated_tasks = []  # Список активных задач
    for task, due_date in tasks:
        due_date_obj = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        if today == due_date_obj:
            print(f"\nВнимание! Сегодня ({today}) пора выполнить задачу: {task}\n")
        elif today > due_date_obj:
            logging.info(f"Задача '{task}' была выполнена или пропущена.")
        else:
            updated_tasks.append((task, due_date))  # Остаются только предстоящие задачи
    save_tasks(updated_tasks)  # Обновляем файл задач

def run_checker(interval_seconds=60):
    """
    Основной цикл проверки задач.
    """
    while True:
        tasks = load_tasks()
        check_and_notify(tasks)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    add_task()           # Добавляем задачу
    show_tasks()         # Показываем все задачи
    run_checker()       # Начинаем фоновый процесс проверки задач
    print()