# Plano de Execução para Agentes de IA

Siga esta ordem cronológica para implementar a aplicação:

## Fase 1: Domínio e Casos de Uso (Python)
1. Crie os *Value Objects* e Entidades centrais (`Answer`, `AnswerSheet`, `CorrectionResult`). Aplique as regras do Object Calisthenics aqui.
2. Crie o Caso de Uso principal: `EvaluateExamUseCase`. Este caso de uso receberá duas abstrações: um extrator de respostas do gabarito e um extrator de respostas do aluno.

## Fase 2: Módulo de Visão Computacional (Adapter)
1. Implemente a interface `AnswerExtractor` usando OpenCV.
2. **Lógica Sugerida para a Imagem:**
   - Carregue a imagem e converta para tons de cinza.
   - Aplique *Thresholding* (binarização) para destacar as linhas e os 'X'.
   - Encontre os contornos da tabela para fatiar a imagem em uma matriz (linhas x colunas).
   - Para cada célula de intersecção (ex: Linha 1, Coluna A), verifique a densidade de pixels pretos. Se passar de um limite X (threshold), considere como marcado.
3. Retorne uma coleção de primeira classe `AnswerSheet` contendo as coordenadas marcadas.

## Fase 3: Camada de API (FastAPI)
1. Configure os endpoints `/upload-gabarito` e `/upload-cartao`.
2. Configure o CORS para permitir requisições do frontend.
3. Crie os validadores de formato de arquivo.
4. Conecte os endpoints ao `EvaluateExamUseCase` e retorne um JSON formatado com a matriz de acertos/erros.

## Fase 4: Interface Web (React)
1. Crie uma estrutura básica de componentes: `<Header />`, `<UploadSection />`, `<ResultsTable />`.
2. Implemente o gerenciamento de estado para armazenar os arquivos selecionados antes do envio.
3. Desenvolva a requisição HTTP e trate os estados de *Loading* e *Error*.
4. Renderize o JSON recebido da API em uma tabela clara, aplicando cores para o status (Verde para Acerto, Vermelho para Erro).