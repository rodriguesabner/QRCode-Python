# Importando as libs
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import pygame

# Construir o analisador de argumentos e analisar os argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="resultado.csv",)  # esse é o arquivo que vai ser salvo com os dados que foram lidos.
args = vars(ap.parse_args())

# Iniciar a stream (iniciar a webcam) e permitir que o sensor da câmera aqueça
print("[INFO] Iniciando o stream e o arquivo .CSV")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# abra o arquivo CSV de saída para gravar e inicializar o conjunto de
# códigos de barras (qr code) encontrados até agora
csv = open(args["output"], "w")
found = set()

# loop sobre a stream
while True:
    # pega o quadro do fluxo de vídeo encadeado e redimensione-o para
    # conter uma largura máxima de 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # encontrar os códigos de barras (qr code) no quadro e decodificar cada um dos códigos de barras
    barcodes = pyzbar.decode(frame)

    # loop sobre os códigos de barras detectados
    for barcode in barcodes:
        # extrair o local da caixa delimitadora do código de barras e desenhar
        # a caixa delimitadora que envolve o código de barras na imagem (nesse caso está verde)
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # os dados do código de barras é um objeto de bytes por isso, se queremos desenhá-lo
        # na nossa imagem de saída, precisamos convertê-lo para uma string primeiro
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # desenha os dados do código de barras e o tipo de código de barras na imagem
        text = "{}".format(barcodeData)
        cv2.putText(frame, '', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # eu não fiz a impressão do texto que contém os dados e etc... caso vc queira mostrar
        # basta trocar o '' por text, ficaria assim \/
        # text = "{} ({})".format(barcodeData, barcodeType)
        # cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # se o texto do código de barras não estiver no nosso arquivo CSV, vai escrever
        # a data e a hora + código de barras no disco e atualizar os dados

        # eu não quis a data e a hora, caso vc queira, basta usar esse código abaixo \/
        # csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))

        if barcodeData not in found:
            # aqui é opcional, eu coloquei só pra avisar que o resultado foi guardado
            # o pygame é responsável por fazer um som tocar
            # pygame.mixer.init()
            # pygame.mixer.music.load('sucess.wav')
            # pygame.mixer.music.play()
            # fim da musica

            csv.write("{}\n".format(barcodeData))
            csv.flush()

            found.clear()
            found.add(barcodeData)

    # Título do Frame
    cv2.imshow("Registro de Ponto", frame)
    key = cv2.waitKey(1) & 0xFF

    # se a tecla `q` foi pressionada, vai interromper o loop e fechar a janela
    if key == ord("q"):
        break

# fecha o arquivo CSV
print("[INFO] Finalizando a stream e fechando o arquivo CSV...")
csv.close()
cv2.destroyAllWindows()
vs.stop()
