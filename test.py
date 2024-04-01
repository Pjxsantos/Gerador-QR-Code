from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
import qrcode
from PIL import Image
import io
import sys

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Gerador de QR Code'
        self.cor_qrcode = "black"
        self.logo_path = None  # Adiciona um caminho para o logo
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QVBoxLayout()
        self.setFixedWidth(350)  # Diminui a largura da interface gráfica

        # Adiciona um título
        self.titulo = QLabel("Gerador de QR Code")
        self.titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centraliza o título
        self.layout.addWidget(self.titulo)

        # Adiciona uma descrição
        self.descricao = QLabel("Escolha a cor do QR Code e insira o \ntexto para gerar o QR Code.")
        self.descricao.setAlignment(Qt.AlignCenter)  # Centraliza a descrição
        self.layout.addWidget(self.descricao)

        # Adiciona um rótulo de dica para os botões de cor
        self.dica_cor = QLabel("Clique em uma cor para selecioná-la:")
        self.layout.addWidget(self.dica_cor)

        # Cria um layout horizontal para os botões de cores
        self.layout_cores = QHBoxLayout()

        cores = ["darkgreen", "darkblue", "black", "red", "brown", "darkmagenta", "darkorange"]
        for cor in cores:
            self.layout_cores.addWidget(self.criar_botao_cor(cor))

        # Adiciona o layout de cores ao layout principal
        self.layout.addLayout(self.layout_cores)

        # Cria um botão para selecionar o logo
        self.botao_logo = QPushButton('Selecionar Logo', self)
        self.botao_logo.clicked.connect(self.selecionar_logo)
        self.layout.addWidget(self.botao_logo)

        # Cria uma entrada de texto
        self.entrada_texto = QLineEdit(self)
        self.layout.addWidget(self.entrada_texto)

        # Cria um botão para gerar o QR Code
        self.botao_gerar = QPushButton('Gerar QR Code', self)
        self.botao_gerar.clicked.connect(self.gerar_qrcode)
        self.botao_gerar.setStyleSheet("background-color: blue; color: white;")  # Pinta o botão de azul
        self.layout.addWidget(self.botao_gerar)

        # Cria uma etiqueta para exibir o QR Code gerado
        self.qr_label = QLabel(self)
        self.qr_label.setFixedSize(327, 327)  # Define o tamanho do quadro para 327x327 pixels
        self.qr_label.setStyleSheet("border: 1px solid black;")  # Adiciona um quadro branco
        self.layout.addWidget(self.qr_label)

        self.setLayout(self.layout)
        self.show()

    def criar_botao_cor(self, cor):
        botao = QPushButton()
        botao.setFixedSize(30, 30)
        botao.setStyleSheet(f"background-color: {cor}")
        botao.clicked.connect(lambda: self.mudar_cor(cor))
        return botao

    def mudar_cor(self, cor):
        self.cor_qrcode = cor

    def selecionar_logo(self):
        self.logo_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Logo", "", "Arquivos de Imagem (*.png *.jpg *.jpeg *.bmp)")

    def gerar_qrcode(self):
        # Obtém o texto da entrada de texto
        texto = self.entrada_texto.text()

        # Verifica se o texto é muito longo para um QR Code
        if len(texto) > 2000:
            QMessageBox.warning(self, "Erro", "O texto é muito longo para um QR Code!")
            return

        # Verifica se o texto está vazio
        if texto.strip() == "":
            QMessageBox.warning(self, "Erro", "Por favor, insira algum texto para gerar o QR Code!")
            return

        try:
            # Cria um objeto QRCode
            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )

            # Adiciona o texto ao QRCode
            qr.add_data(texto)
            qr.make(fit=True)

            # Cria uma imagem do QRCode
            img = qr.make_image(fill_color=self.cor_qrcode, back_color="white").convert('RGB')

            if self.logo_path is not None:
                logo = Image.open(self.logo_path)
                qr_size = img.size[0]
                logo_size = int(qr_size * 0.3)  # Diminui o tamanho do logo em 30%
                logo_pos = (qr_size - logo_size) // 2  # Centraliza o logo
                box = (logo_pos, logo_pos, logo_pos + logo_size, logo_pos + logo_size)

                logo = logo.resize((box[2] - box[0], box[3] - box[1]))
                img.paste(logo, box)

            # Converte a imagem em um formato de bytes
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format="PNG")
            img_byte_array = img_byte_array.getvalue()

            # Cria uma imagem QPixmap a partir dos bytes
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_array)

            # Exibe a imagem na etiqueta
            self.qr_label.setPixmap(pixmap.scaled(327, 327, Qt.KeepAspectRatio))

            # Salva a imagem como um arquivo PNG
            file_path, _ = QFileDialog.getSaveFileName(self, "Salvar QR Code", "", "Arquivos PNG (*.png)")
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(img_byte_array)
                QMessageBox.information(self, "Sucesso", "QR Code criado com sucesso!")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            QMessageBox.warning(self, "Erro", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
