import dropbox
import os
from PIL import Image
ACCESS_TOKEN = "sl.u.AFs-UnWZWUn5EA9xwPDDm5pcFU76a8bUAEMa4AWoucx3VZ4UkTsLKXw_ShRlq3bBlvyHToXcUk3pbjSJxsmtv-qXJ5KJD3xapYZikj3eGEbd7NeWVmwn5pJ5BMXklMXzOPQ7JYRsyGG1kjWRu1oStdEaf6Xj3VMKGbvqiTl7a0bmjsOoKAliyY_EBuo4_ALaoskU-Of-HCFCoV6q88gF0zsWA2-3nMWfpo4HiO1dDsBp0qRri8nMQyoTPqsb6ZR1L2XXxvVQYrSB-Zi6L0xLtXUril87J86gVUch1qDt95AHRDvgH3wKx23M2LuHN7Vr4muak2MSE5iNUUImPNq1unJ2dzGPkyrxA6lYjCOYlYC5xkt4nVlzq7RbGYTbMquehi9DYJSGwsf13txGeQYlQpFqdY7Iv7uXGspeQWSbmKstLP_lk8chZod9toyDZPX_Yt_0JsJEgDkeuXje48N8j1eSXfI6c04MlCk71jwzgDANZUVrkTd9Afnko_BCD0bMFVBxkjP0pztK3QgW6eTY9TCJkxnTaBhXgMQ3LCUhImjX5tw_gSTdMHQo7K1k9N-4YtjgzIJMdUDQusLzl0R8XFo81qAOvOGP_baqVspKIpKTCPffK00RxMm2BCCmiQp3In4Ah2fNVH3uG3n924GNwaERk_Z0K-kh20QvRqb8g_nFXHwGzdCyXZ2QmiST0rRC2q66mZg9GX7XT7Y6NgT_BfdHgbOU9z6TT61Y8zamnqyHLXksaUZP6ne9UoY_kkAz1b2plQk90iJKII1KxNRKUUYsBrYT36yVKT0cqVmmYTn2uhzhT8P1WZfZdL-1fCC5Db7ByINiIQeTpePySV7d6JQ4vyaouIpULFRfGkMZ41u8LuzbHghL8cLCqJIrvcBRNrxSnfAkB9GL2ggfecgaiSP_v2zyV0mkPWcOjfOACmDkpgFB8cz2pPJ1UPz3whBtiYJb_HjmAQvFhmkwNq-_-_ty_pn00cSW-ZsMmDI943qunpbdqdEwWrfu6rSRKk2t8fqG7XKU1rvtYMzOFISQM4GrznPptv2phEvNPIC91-mlBvv1eH6xJs9WDlGetr451Sw87cjusD4vAuQ27TiQTGiutXpMhQx-0C3GqAdgp4OvQQ_RNmuTTyZi1YAnddQzWcCGd9bA_o15wAzqdIefmzY5YOumkqt0q0Wyh8thsfjI0ZAGfE1joxAsYU4SmLkpEseYCQZFTPLHdcnslArtliB721pGD1DEuO05pVfg7R4DzyL4mYWxY0gQyuHRzL3brvwAuIOWZVqNX4QuHxA5rhR_MJrxhEFI4AOODbi9_L06TA4_4sXiA-rocmaXCCa0vhZBOAb8P3V2XO3WU_DEoyrkRrNM-l_KUNOH5qnmf5LtxYUnrNaQkeWiWqcm40ntysHSp98rdcjU8a657S8iOoMycMB6cmV8yrIdPRDtOOHLxfe6cbKKoeQx4Quws2sdj-M"
dbx = dropbox.Dropbox(ACCESS_TOKEN)

def list_files_recursive(folder_path):
    try:
        result = dbx.files_list_folder(folder_path, recursive=True)
        entries = result.entries

        while result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
            entries.extend(result.entries)

        return entries
    except dropbox.exceptions.ApiError as err:
        print(f"Erro ao acessar a pasta: {err}")
        return []

def download_file(file_path, save_path):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        dbx.files_download_to_file(save_path, file_path)
        print(f"Dados do aluno {os.path.basename(save_path).replace('.jpg','')} foram salvos com sucesso.")
        print("-----------------------------------------------------")
    except dropbox.exceptions.ApiError as err:
        print(f"Erro ao baixar o arquivo {file_path}: {err}")

def baixar_dados_alunos(folder_path, download_directory):
    files = list_files_recursive(folder_path)

    for entry in files:
        if isinstance(entry, dropbox.files.FileMetadata):
            file_name = entry.name
            file_path = entry.path_display

            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Remove o prefixo da pasta raiz para evitar duplicação
                relative_path = os.path.relpath(file_path, folder_path)
                local_path = os.path.join(download_directory, relative_path)
                
                print(f"Baixando dados do aluno: {file_name}...")
                download_file(file_path, local_path)

