import os
import csv
from datetime import datetime

quem_ja_foi_marcado = []

def retornar_quem_veio(turma, dados_legiveis=False):
    caminho_csv = os.path.join(turma, f"{turma}.csv")
    resultado = []

    if not os.path.exists(caminho_csv):
        return resultado

    with open(caminho_csv, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            nome = linha["nome"].lower()
            status = linha["presença"]
            if dados_legiveis:
                resultado.append(nome)
                resultado.append("Sim" if status.lower() == "t" else "Não")
            else:
                resultado.append([nome, status, linha["data_hora"]])

    return resultado

def marcar_quem_veio(turma: str, nome: str, veio: bool):
    nome = nome.lower()
    
    if nome in quem_ja_foi_marcado:
        print("Já reconhecido! ({})".format(nome))
    else:
        status = "Sim" if veio else "Não"
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        caminho_pasta = turma
        caminho_csv = os.path.join(caminho_pasta, f"{turma}.csv")

        # Cria a pasta se não existir
        os.makedirs(caminho_pasta, exist_ok=True)

        # Verifica se o CSV já existe para escrever cabeçalho
        escrever_cabecalho = not os.path.exists(caminho_csv)

        with open(caminho_csv, mode='a', newline='', encoding='utf-8') as arquivo:
            writer = csv.DictWriter(arquivo, fieldnames=["nome", "presença", "data_hora"])
            if escrever_cabecalho:
                writer.writeheader()
            writer.writerow({"nome": nome, "presença": status, "data_hora": data_hora})

        quem_ja_foi_marcado.append(nome)

    

