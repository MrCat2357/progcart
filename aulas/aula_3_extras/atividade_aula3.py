import wget
import os

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

class IBGE(Downloader):
    def __init__(self, destination_folder):
        server_url_format = "https://geoftp.ibge.gov.br/cartas_e_mapas/folhas_topograficas/vetoriais/escala_1000mil/shapefile/{name}"
        super().__init__(server_url_format, destination_folder)
        
    def download_data(self, file_name):
        self.download(file_name)

# Exemplo de uso
if __name__ == "__main__":
    # Defina a pasta de destino
    destination_folder = "C:/Users/catul/Downloads/"

    # Criação do objeto IBGE
    ibge_downloader = IBGE(destination_folder)

    # Baixando um arquivo específico
    file_name = "g04_na19.zip"  # Substitua pelo nome do arquivo real
    ibge_downloader.download_data(file_name)
 