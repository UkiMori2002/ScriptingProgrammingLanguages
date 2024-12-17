import sys
import time
import sqlite3
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QProgressBar, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

# это класс для выполнения HTTP-запросов в фоновом режиме
class FetchDataThread(QThread):
    update_progress = pyqtSignal(int)  # сигнал для обновления прогресса
    data_fetched = pyqtSignal(list)  # сигнал для пердачи данных

    def run(self):
        url = 'https://jsonplaceholder.typicode.com/posts'
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            for i in range(len(posts)):
                time.sleep(0.1)  # бурная имитация задержки
                self.update_progress.emit((i + 1) * 100 // len(posts))
            self.data_fetched.emit(posts)
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")

# ккласс для сохранения данных в бд в фоновом режиме
class SaveDataThread(QThread):
    update_progress = pyqtSignal(int)  # сигнал для обновления прогресса
    data_saved = pyqtSignal()  # сигнал для уведомления о завершении

    def __init__(self, posts):
        super().__init__()
        self.posts = posts

    def run(self):
        # создаем новое соединение с базой данных в этом потоке
        conn = sqlite3.connect('posts.db')
        cursor = conn.cursor()

        for i, post in enumerate(self.posts):
            time.sleep(0.1)  # имитация задержки
            cursor.execute('''
                INSERT OR IGNORE INTO posts (id, user_id, title, body)
                VALUES (?, ?, ?, ?)
            ''', (post['id'], post['userId'], post['title'], post['body']))
            conn.commit()
            self.update_progress.emit((i + 1) * 100 // len(self.posts))

        # закрываем соединение с базой данных
        conn.close()
        self.data_saved.emit()

# главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Многозадачность в PyQt5")
        self.setGeometry(100, 100, 600, 400)

        # основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # макет
        self.layout = QVBoxLayout(self.central_widget)

        # кнопка для загрузки данных
        self.load_button = QPushButton("Загрузить данные", self)
        self.load_button.clicked.connect(self.start_fetching)
        self.layout.addWidget(self.load_button)

        # индикатор выполнения
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        # метка для отображения статуса
        self.status_label = QLabel("Готово", self)
        self.layout.addWidget(self.status_label)

        # таблица для отображения данных
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["ID", "User ID", "Title", "Body"])
        self.layout.addWidget(self.table_widget)

        # таймер для периодической проверки обновлений
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_updates)
        self.timer.start(15000)  # запускаем таймер каждые 10 секунд

    def start_fetching(self):
        """Запускает загрузку данных в фоновом потоке."""
        self.status_label.setText("Загрузка данных...")
        self.progress_bar.setValue(0)

        # создаем и запускаем поток для загрузки данных
        self.fetch_thread = FetchDataThread()
        self.fetch_thread.update_progress.connect(self.update_progress)
        self.fetch_thread.data_fetched.connect(self.save_data)
        self.fetch_thread.start()

    def save_data(self, posts):
        """Сохраняет данные в базу данных в фоновом потоке."""
        self.status_label.setText("Сохранение данных...")
        self.progress_bar.setValue(0)

        # создаем и запускаем поток для сохранения данных
        self.save_thread = SaveDataThread(posts)
        self.save_thread.update_progress.connect(self.update_progress)
        self.save_thread.data_saved.connect(self.update_ui)
        self.save_thread.start()

    def update_progress(self, value):
        """Обновляет индикатор выполнения."""
        self.progress_bar.setValue(value)

    def update_ui(self):
        """Обновляет интерфейс после завершения сохранения данных."""
        self.status_label.setText("Данные успешно сохранены")
        self.progress_bar.setValue(100)

        # обновляем таблицу данных
        self.load_data_from_db()

    def load_data_from_db(self):
        """Загружает данные из базы данных и отображает их в таблице."""
        conn = sqlite3.connect('posts.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        conn.close()

        # очищаем таблицу
        self.table_widget.setRowCount(0)

        # заполняем таблицу данными
        for post in posts:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(str(post[0])))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(post[1])))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(post[2]))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(post[3]))

    def check_for_updates(self):
        """Периодическая проверка обновлений на сервере."""
        self.status_label.setText("Проверка обновлений...")
        self.start_fetching()

# запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
