import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QWidget, QTextEdit

# Главное окно приложения
class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ данных с использованием pandas и matplotlib")
        self.setGeometry(100, 100, 800, 600)

        # основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # макет
        self.layout = QVBoxLayout(self.central_widget)

        # кнопка для загрузки данных
        self.load_button = QPushButton("Загрузить данные из CSV", self)
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        # поле для отображения статистики
        self.stats_text = QTextEdit(self)
        self.stats_text.setReadOnly(True)
        self.layout.addWidget(self.stats_text)

        # выбор типа графика
        self.plot_type_combo = QComboBox(self)
        self.plot_type_combo.addItems(["Линейный график", "Гистограмма", "Круговая диаграмма"])
        self.plot_type_combo.currentIndexChanged.connect(self.update_plot)
        self.layout.addWidget(self.plot_type_combo)

        # поле для отображения графика
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # кнопка для добавления значения на график
        self.add_value_button = QPushButton("Добавить значение", self)
        self.add_value_button.clicked.connect(self.add_value_to_plot)
        self.layout.addWidget(self.add_value_button)

        # иннициализация данных
        self.data = None

    def load_data(self):
        """Загрузка данных из CSV-файла."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть CSV-файл", "", "CSV Files (*.csv)")
        if file_path:
            self.data = pd.read_csv(file_path)
            self.display_stats()
            self.update_plot()

    def display_stats(self):
        """Отображение статистики по данным."""
        if self.data is not None:
            stats = f"Количество строк: {self.data.shape[0]}\n"
            stats += f"Количество столбцов: {self.data.shape[1]}\n"
            stats += f"Минимальное значение в 'Value1': {self.data['Value1'].min()}\n"
            stats += f"Максимальное значение в 'Value1': {self.data['Value1'].max()}\n"
            stats += f"Среднее значение в 'Value1': {self.data['Value1'].mean()}\n"
            stats += f"Медиана в 'Value1': {self.data['Value1'].median()}\n"
            self.stats_text.setText(stats)

    def update_plot(self):
        """Обновление графика в зависимости от выбранного типа."""
        if self.data is not None:
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            if self.plot_type_combo.currentText() == "Линейный график":
                ax.plot(self.data['Date'], self.data['Value1'], label='Value1')
                ax.set_title('Линейный график')
                ax.set_xlabel('Дата')
                ax.set_ylabel('Значение')
                ax.legend()

            elif self.plot_type_combo.currentText() == "Гистограмма":
                ax.bar(self.data['Date'], self.data['Value2'], label='Value2')
                ax.set_title('Гистограмма')
                ax.set_xlabel('Дата')
                ax.set_ylabel('Значение')
                ax.legend()

            elif self.plot_type_combo.currentText() == "Круговая диаграмма":
                category_counts = self.data['Category'].value_counts()
                ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')
                ax.set_title('Круговая диаграмма')

            self.canvas.draw()

    def add_value_to_plot(self):
        """Добавление нового значения на график."""
        if self.data is not None:
            new_date = input("Введите новую дату (в формате YYYY-MM-DD): ")
            new_value1 = float(input("Введите новое значение для Value1: "))
            new_value2 = float(input("Введите новое значение для Value2: "))
            new_category = input("Введите новую категорию: ")

            # добвление новых данных в DataFrame
            new_row = pd.DataFrame({'Date': [new_date], 'Value1': [new_value1], 'Value2': [new_value2], 'Category': [new_category]})
            self.data = pd.concat([self.data, new_row], ignore_index=True)

            # обновляем статистику и график
            self.display_stats()
            self.update_plot()

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    window.show()
    sys.exit(app.exec_())
