# 🛡️ Monitoramento de Ameaças em Python

Este projeto é uma ferramenta de monitoramento de diretórios desenvolvida para times de **SOC (Security Operations Center)**. Ele detecta alterações em um diretório específico, como criação, modificação e exclusão de arquivos, e exibe os logs em uma interface gráfica intuitiva. 🖥️

---

## 🚀 Funcionalidades

- **📂 Seleção de diretório**: Escolha o diretório que deseja monitorar.
- **🔍 Detecção de alterações**: Identifica criação, modificação e exclusão de arquivos.
- **🔢 Cálculo de hash MD5**: Gera um hash MD5 para cada arquivo modificado ou criado, permitindo a verificação de integridade.
- **🖼️ Interface gráfica**: Exibe logs em tempo real em uma interface amigável.
- **💾 Salvar logs**: Opção para salvar os logs em um arquivo de texto.

---

## 🛠️ Como Usar

### 📋 Pré-requisitos

- Python 3.x instalado.
- Bibliotecas necessárias: `watchdog` e `tkinter`.

### ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/monitoramento-ameacas.git
