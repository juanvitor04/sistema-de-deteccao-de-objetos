# 📱 **Detecção de objetos com YOLO e Armazenamento SMB**

Este projeto realiza a detecção de objetos utilizando o modelo YOLO e armazena as imagens detectadas em um servidor SMB.

---

## 🔧 **Requisitos**

Antes de começar, verifique se você tem as seguintes dependências instaladas:

- **Python 3.x**
- **OpenCV**
- **YOLO** (You Only Look Once)
- **SMBClient**

---

## 🛠️ **Instalação**

### 1. **Clonando o Repositório**
Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/juanvitor04/hello-world/edit/main/README.md
cd seu-repositorio

pip install ultralytics
pip install smbprotocol

Configuração do Usuário SMB

sudo apt update
sudo apt install samba
sudo useradd -m usuario_smb
sudo passwd usuario_smb
sudo smbpasswd -a usuario_smb
sudo nano /etc/samba/smb.conf

insira essas configurações no arquivo smb.conf

[SharedFolder]
   path = /path/to/shared/folder
   browseable = yes
   writable = yes
   guest ok = no
   valid users = vitor
   create mask = 0700
   directory mask = 0700
[global]
   server min protocol = SMB2
   server max protocol = SMB3
   encrypt passwords = yes
   smb encrypt = required

Crie as variáveis de ambiente

setx SAMBA_PASSWORD "usuario"
setx SAMBA_PASSWORD "senha"

Espero que isso ajude! Se precisar de mais alguma coisa, estou por aqui. 😄
