import wget
import os
import zipfile

class Downloader:
    def __init__(self, server_url_format, destination_folder):
        self.server_url_format = server_url_format
        self.destination_folder = destination_folder

    def download(self, file_name):
        url = self.server_url_format.format(name=file_name)
        file_path = os.path.join(self.destination_folder, file_name)
        
        # Verificar se o diretório de destino existe, se não, criar
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)
        
        print(f"Iniciando o download de {url}...")
        wget.download(url, file_path)
        print(f"\nArquivo {file_name} baixado com sucesso para {file_path}.")

        # Descompactar o arquivo, se for um ZIP
        if file_name.endswith(".zip"):
            self.unzip_file(file_path)

    def unzip_file(self, zip_path):
        # Verificar se o arquivo ZIP existe
        if zipfile.is_zipfile(zip_path):
            print(f"Descompactando {zip_path}...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.destination_folder)
            print(f"Arquivo {zip_path} descompactado com sucesso.")
            # Após descompactar, você pode opcionalmente excluir o arquivo ZIP
            os.remove(zip_path)
        else:
            print(f"O arquivo {zip_path} não é um arquivo ZIP válido.")

class IBGE(Downloader):
    def __init__(self, destination_folder):
        server_url_format = "https://geoftp.ibge.gov.br/cartas_e_mapas/folhas_topograficas/vetoriais/escala_1000mil/shapefile/{name}"
        super().__init__(server_url_format, destination_folder)
        
    def download_data(self, file_name):
        self.download(file_name)

# Exemplo de uso
if __name__ == "__main__":
    # Defina a pasta de destino
    destination_folder = "C:/Program Files/QGIS 3.40.3/apps/qgis/resources/data/camadas_ibge/"

    # Criação do objeto IBGE
    ibge_downloader = IBGE(destination_folder)

    # Baixando um arquivo específico
    file_name = "g04_na19.zip"  # Substitua pelo nome do arquivo real
    ibge_downloader.download_data(file_name)
