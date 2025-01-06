import cv2
import datetime
import time
from ultralytics import YOLO
import threading
import os
import smbclient

# Carregar o modelo YOLO
modelo = YOLO('yolo11n.pt')

# Definir o índice para a classe "celular"
CELULAR_CLASS_INDEX = 67

# Variável para controlar o loop de detecção
executando = False

# Obter as variáveis de ambiente para autenticação
samba_username = os.getenv('SAMBA_USERNAME')
samba_password = os.getenv('SAMBA_PASSWORD')
samba_server = '192.168.1.101'
samba_share_name = 'SharedFolder'
samba_share_path = f'\\\\{samba_server}\\{samba_share_name}'

# Verificar se as variáveis de ambiente estão definidas
if not samba_username or not samba_password:
    print("As variáveis de ambiente SAMBA_USERNAME e SAMBA_PASSWORD devem estar definidas.")
    exit()

# Configurar o cliente SMB
smbclient.ClientConfig(username=samba_username, password=samba_password)

def iniciar_detecao():
    global executando
    executando = True
    thread_detecao = threading.Thread(target=detectar_celulares)
    thread_detecao.start()

def parar_detecao():
    global executando
    executando = False

def detectar_celulares():
    # Capturar vídeo da webcam
    captura_video = cv2.VideoCapture(0)
    captura_video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    captura_video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    captura_video.set(cv2.CAP_PROP_FPS, 30)  # Alterar para 30 FPS

    ultimo_tempo_captura = time.time()

    while executando:
        ret, quadro = captura_video.read()
        
        if not ret:
            print("Não foi possível capturar o quadro.")
            break

        tamanho_img = 640  # Resolução menor para o input do modelo

        # Realizar a detecção usando o modelo YOLO
        resultados = modelo(quadro, imgsz=tamanho_img)

        celular_detectado = False

        for resultado in resultados:
            caixas = resultado.boxes
            for caixa in caixas:
                id_classe = int(caixa.cls[0].item())
                
                # Verifique se a classe detectada é um celular
                if id_classe == CELULAR_CLASS_INDEX:
                    x1, y1, x2, y2 = caixa.xyxy[0].numpy()
                    confianca = caixa.conf[0].item()
                    rotulo = f'Celular: {confianca*100:.2f}%'
                    cv2.rectangle(quadro, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(quadro, rotulo, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    celular_detectado = True
        
        # Salvar uma imagem por segundo se um celular for detectado
        if celular_detectado and (time.time() - ultimo_tempo_captura >= 1):
            ultimo_tempo_captura = time.time()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            nome_arquivo = f'celular_detectado_{timestamp}.jpg'
            caminho_completo = os.path.join(samba_share_path, nome_arquivo)
            cv2.putText(quadro, timestamp, (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Salvar a imagem no compartilhamento Samba
            with smbclient.open_file(caminho_completo, mode='wb') as file:
                file.write(cv2.imencode('.jpg', quadro)[1].tobytes())
            
            print(f'Imagem salva no Samba: {caminho_completo}')

        cv2.imshow('Detecção de Celulares', quadro)

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    captura_video.release()
    cv2.destroyAllWindows()

# Iniciar a detecção
iniciar_detecao()

# A detecção vai continuar até que o script seja interrompido manualmente
# Para parar a detecção, você pode chamar parar_detecao() em outro lugar do seu código
