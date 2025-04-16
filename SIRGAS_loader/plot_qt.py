import sys
from PyQt5 import QtWidgets, uic, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from sirgas_downloader import sirgas_downloader  # Seu downloader
from sirgas_dataframe import read_sirgas_dataframe


class ColumnSelectorDialog(QtWidgets.QDialog):
    def __init__(self, columns, selected_columns=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selecionar Colunas")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        for col in columns:
            item = QtWidgets.QListWidgetItem(col)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked if not selected_columns or col in selected_columns else QtCore.Qt.Unchecked)
            self.list_widget.addItem(item)

        self.layout.addWidget(self.list_widget)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

    def get_selected_columns(self):
        return [
            self.list_widget.item(i).text()
            for i in range(self.list_widget.count())
            if self.list_widget.item(i).checkState() == QtCore.Qt.Checked
        ]


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("plot.ui", self)  # Certifique-se que todos os objetos existem

        # Canvas do gráfico
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QtWidgets.QVBoxLayout()
        self.groupBox.setLayout(layout)
        layout.addWidget(self.canvas)

        # Conectar botões
        self.pushButton.clicked.connect(self.on_plot_button_clicked)
        self.pushButton_2.clicked.connect(self.on_table_button_clicked)
        self.selectColumnsButton.clicked.connect(self.select_columns_dialog)
        self.downloadButton.clicked.connect(self.on_download_button_clicked)  # Novo botão para download

        self.gdf = None
        self.selected_columns = None  # Colunas escolhidas pelo usuário

    def load_data(self):
        if self.gdf is None:
            test_obj = sirgas_downloader()
            saved_file_name = test_obj.download(test_obj.multianual_coord_url)
            decompressed_crd_file = test_obj.decompress(saved_file_name)
            self.gdf = read_sirgas_dataframe(decompressed_crd_file)

    def select_columns_dialog(self):
        self.load_data()

        columns = self.gdf.drop(columns="geometry").columns.tolist()
        dialog = ColumnSelectorDialog(columns, self.selected_columns, self)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.selected_columns = dialog.get_selected_columns()

    def on_plot_button_clicked(self):
        self.load_data()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.gdf.plot(ax=ax, color='blue', markersize=10)
        self.canvas.draw()

    def on_table_button_clicked(self):
        self.load_data()

        df = self.gdf.drop(columns='geometry')

        if self.selected_columns:
            df = df[self.selected_columns]

        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

    def on_download_button_clicked(self):
        # Captura a URL da QLineEdit
        url = self.urlLineEdit.text()
        if url:
            # Passa a URL para o downloader
            test_obj = sirgas_downloader()
            saved_file_name = test_obj.download(url)  # Usa a URL fornecida
            decompressed_crd_file = test_obj.decompress(saved_file_name)
            self.gdf = read_sirgas_dataframe(decompressed_crd_file)
            QtWidgets.QMessageBox.information(self, "Download Concluído", "Download e decomposição concluídos!")
        else:
            QtWidgets.QMessageBox.warning(self, "Erro", "Por favor, insira uma URL válida.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())
