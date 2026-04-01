# Escopo do Projeto: Sistema de Correção Automática de Provas (OCR/OMR)

## 1. Visão Geral
O projeto consiste em uma aplicação web desenvolvida para automatizar a correção de cartões-resposta de provas de múltipla escolha. O sistema utilizará processamento de imagem e Reconhecimento Óptico de Caracteres (OCR) / Reconhecimento Ótico de Marcas (OMR) para ler imagens digitalizadas contendo uma grade de respostas (ex: Linhas 1-7, Colunas A-E com marcação 'X').

## 2. Requisitos Funcionais
- **Upload de Gabarito:** O usuário deve poder fazer upload do gabarito oficial (podendo ser um arquivo JSON/CSV ou uma imagem do cartão mestre).
- **Upload de Cartão-Resposta:** O usuário deve poder fazer upload da imagem do cartão-resposta do aluno (formatos PNG, JPG, JPEG).
- **Processamento de Imagem:** O sistema deve identificar a grade (linhas numéricas e colunas alfabéticas) e detectar a presença de marcações ('X' ou preenchimento) nas células.
- **Correção Automática:** O sistema deve comparar as marcações extraídas do cartão do aluno com o gabarito.
- **Visualização de Resultados:** A interface deve exibir uma tabela clara contendo a questão, a resposta do aluno, a resposta correta e o status (Acerto/Erro).

## 3. Requisitos Não Funcionais
- **Acessibilidade:** Interface web simples, intuitiva e amigável.
- **Performance:** O processamento da imagem e o retorno da correção devem ocorrer em poucos segundos.
- **Manutenibilidade:** Código estruturado seguindo Clean Architecture, princípios SOLID e Object Calisthenics.