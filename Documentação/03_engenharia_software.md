# Diretrizes de Engenharia de Software

Agentes de IA devem estritamente seguir estas regras durante a geração e refatoração do código:

## 1. Princípios SOLID
- **SRP (Single Responsibility Principle):** Classes devem ter um único motivo para mudar. Ex: A classe que lê a imagem (`ImageReader`) não deve ser a mesma que compara as respostas (`GradeCalculator`).
- **OCP (Open/Closed Principle):** O sistema de extração deve ser aberto para extensão (ex: adicionar suporte a um novo formato de cartão-resposta) sem modificar o código existente, utilizando interfaces ou classes abstratas (`AnswerExtractor`).
- **LSP (Liskov Substitution Principle):** Qualquer implementação de extrator de imagem deve poder substituir a abstração base sem quebrar o sistema.
- **ISP (Interface Segregation Principle):** Interfaces pequenas e específicas (ex: `IImageUploader`, `IResultPresenter`).
- **DIP (Dependency Inversion Principle):** Casos de uso de correção não devem depender diretamente do OpenCV, mas sim de uma porta (interface) de serviço de visão computacional.

## 2. Object Calisthenics (Regras Críticas)
Para garantir um código elegante e sustentável, aplique as seguintes regras:
1. **Apenas um nível de indentação por método:** Extraia lógicas complexas para submétodos privados.
2. **Não use a palavra-chave `else`:** Utilize *Early Returns* (cláusulas de guarda).
3. **Envolva todos os primitivos e strings:** Crie *Value Objects* para conceitos de domínio. (Ex: Em vez de usar `string` para a resposta, crie uma classe `AnswerChoice`).
4. **Coleções de Primeira Classe:** Qualquer classe que contenha uma coleção (como uma lista de respostas) não deve conter outros comportamentos (Ex: Uma classe `AnswerSheet` que encapsula `List<Answer>`).
5. **Um ponto por linha:** Evite encadeamento excessivo de métodos (Law of Demeter).
6. **Não abrevie:** Nomes de variáveis, métodos e classes devem ser descritivos (ex: use `studentAnswerSheet` em vez de `sas`).
7. **Mantenha entidades pequenas:** Limite de linhas por classe e pacote.
8. **Nenhuma classe com mais de duas variáveis de instância:** Agrupe variáveis altamente coesas em novos objetos.
9. **Nenhum Getter/Setter explícito (Tell, Don't Ask):** O objeto deve executar operações com seus próprios dados. Em vez de `sheet.getAnswers()`, use `sheet.compareWith(gabarito)`.