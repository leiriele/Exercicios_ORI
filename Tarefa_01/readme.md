Geração de um Sistema de ORI  

Escreveremos um programa usando Python. Para cada fase entregar: 

O fonte em python, 

A listagem dos resultados em .txt, 

Um relatório PDF, padrão ABNT, com capa e sumário, descrição do problema, limitações e estruturas de dados, funções utilizadas.   

Apresentação de seminário sobre a tarefa desenvolvida. 

Descrição do problema 

Dados vários arquivos de documento em formato PDF contendo texto. (arquivos no Moodle) 

Para cada arquivo:

- Extrair todas as palavras gerando uma lista contendo todas as ocorrências de cada palavra para cada documento. Estas palavras devem estar em minúsculas contendo somente letras. Considerar acentos e cedilha.

- Extrair as stopwords, por supervisão. Incluir verbos. 

- Listar as stopwords encontradas.

- ordenar, tirar plural, aumentativos, diminutivos e gênero. Contar frequências, associar docid.

    - Listar os termos seguidos de 2 números (código do documento e frequência).  

- Gerar as estruturas Lista de documentos (gerado na leitura da pasta de documentos), Dicionário de termos e Postings, criando a estrutura Índice Invertido.

- Salvar esta estrutura em arquivo.(Termo,freq,(docid, freq,)) 

Implementação  

A solução deve possuir regras e lista de exceções, adequadas ao conjunto de palavras fornecido.  
