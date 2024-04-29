import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Define o nome do arquivo a ser baixado
file_name = 'plano-financeiro-pn-eduardo-carreiro.xlsx'

# Define o ID da pasta onde o arquivo está localizado
folder_id = '1FsDLf_ClpwSMKcm_AK4avXNo0TQWNllc'

# Define o caminho local onde o arquivo será salvo
local_path = './arquivosalvo'

# Carrega as credenciais a partir do arquivo token.json
creds = Credentials.from_authorized_user_file('token.json')

# Cria um objeto de serviço para a API do Google Drive
service = build('drive', 'v3', credentials=creds)

# Define os parâmetros para a consulta de busca do arquivo
query = f"name='{file_name}' and '{folder_id}' in parents"
response = service.files().list(q=query).execute()

# Verifica se o arquivo foi encontrado
files = response.get('files', [])
if not files:
    print(f'O arquivo "{file_name}" não foi encontrado na pasta com ID "{folder_id}".')
else:
    # Obtém o ID do arquivo encontrado
    file_id = files[0]['id']

    # Define o caminho completo para salvar o arquivo localmente
    download_path = os.path.join(local_path, file_name)

    # Faz o download do arquivo
    request = service.files().get_media(fileId=file_id)
    with open(download_path, 'wb') as file:
        downloader = request.execute()
        file.write(downloader)

    print(f'O arquivo "{file_name}" foi baixado com sucesso para "{download_path}".')
