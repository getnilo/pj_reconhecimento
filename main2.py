import cv2
import face_recognition
import os
import a
import sys
import main
import conversor as cv

mostrar_janela = False
try:
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-mostrar':
            mostrar_janela = True

        elif sys.argv[1] == '-baixar':
            main.baixar_dados_alunos(f"/{str(sys.argv[2])}",f"{str(sys.argv[2])}")
            exit()
        else:
            print("Parametro disconhecido.")
            exit()

    elif len(sys.argv) > 3:
        print("""Muitos argumentos.""")
        exit()

    else:
        pass

except Exception as e:
    print("Error: "+e)

turma_selec = str(input('Turma (nome da pasta): '))
alunos_ja_identificados = []

def carregar_rostos_conhecidos(pasta=turma_selec):
    rostos_codificados = []
    nomes = []

    for nome_aluno in os.listdir(pasta):
        caminho_aluno = os.path.join(pasta, nome_aluno)
        if not os.path.isdir(caminho_aluno):
            continue

        for imagem_nome in os.listdir(caminho_aluno):
            if imagem_nome.endswith(('.png', '.jpg', '.jpeg')):
                caminho_imagem = os.path.join(caminho_aluno, imagem_nome)
                imagem = face_recognition.load_image_file(caminho_imagem)
                codificacoes = face_recognition.face_encodings(imagem)

                if codificacoes:
                    rostos_codificados.append(codificacoes[0])
                    nomes.append(nome_aluno.lower())

    return rostos_codificados, nomes

rostos_conhecidos, nomes_conhecidos = carregar_rostos_conhecidos()

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    frame_pequeno = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)

    localizacoes_rostos = face_recognition.face_locations(rgb_frame)
    codificacoes_rostos = face_recognition.face_encodings(rgb_frame, localizacoes_rostos)

    for (top, right, bottom, left), codificacao in zip(localizacoes_rostos, codificacoes_rostos):
        distancias = face_recognition.face_distance(rostos_conhecidos, codificacao)

        if len(distancias) == 0:
            continue

        menor_dist = min(distancias)
        indice_mais_proximo = distancias.tolist().index(menor_dist)

        nome = "Desconhecido"

        if menor_dist < 0.4:
            nome = nomes_conhecidos[indice_mais_proximo]

            if nome not in alunos_ja_identificados:
                print(f"Aluno {nome} foi identificado (distância: {menor_dist:.2f})")
                alunos_ja_identificados.append(nome)
                a.marcar_quem_veio(turma_selec, nome, veio=True)
        else:
            print(f"Pessoa não registrada (distância mínima: {menor_dist:.2f})")

        if mostrar_janela:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cor_caixa = (0, 255, 0) if nome != "Desconhecido" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), cor_caixa, 2)
            cv2.putText(frame, nome, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_caixa, 2)

    if mostrar_janela:
        cv2.imshow('Reconhecimento Facial', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv.convert(os.path.join(turma_selec,turma_selec+".csv"),os.path.join(turma_selec,turma_selec+".xlsx"))
        break

video_capture.release()
cv2.destroyAllWindows()
