# Stack Tecnológico

Para atingir os objetivos de performance, componentização e facilidade de manutenção, o projeto utilizará a seguinte stack:

## 1. Backend (Python)
- **Framework Web:** FastAPI (Escolhido por sua alta performance, tipagem estática nativa com Pydantic e facilidade em criar endpoints RESTful limpos).
- **Processamento de Imagem (OMR/OCR):** - `OpenCV` (cv2): Para pré-processamento da imagem (conversão para escala de cinza, binarização, detecção de contornos e alinhamento da grade).
  - `Pytesseract` (ou rotinas de detecção de área de contorno do OpenCV): Para identificar a marcação de 'X' na grade de coordenadas.
- **Gerenciamento de Dependências:** Poetry ou Pipenv.

## 2. Frontend
- **Framework/Biblioteca:** React (Permite a criação de uma SPA leve e responsiva, facilitando o gerenciamento de estado dos arquivos enviados e da tabela de resultados).
- **Estilização:** Tailwind CSS (Para criar a interface simples e amigável de forma rápida e com código limpo).
- **Comunicação com API:** Axios ou Fetch API.

## 3. Padrões de Projeto e Arquitetura
- **Clean Architecture:** Separação clara entre a camada de Domínio, Casos de Uso, Controladores (API) e Adaptadores Externos (Visão Computacional).