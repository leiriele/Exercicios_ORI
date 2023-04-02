import os
import re
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
# from nltk.stem import WordNetLemmatizer
import inflect
import pandas as pd
import spacy

# nltk.download('wordnet')

# Criando o objeto lematizador
# lemmatizer = WordNetLemmatizer()

# Definir a lista de stopwords e pontuações que serão removidas dos documentos
stop_words = set(stopwords.words('portuguese'))

stop_words.update(['.', ',', '"', "'", '?', '!', ':',
                  ';', '(', ')', '[', ']', '{', '}'])

# Definir o stemmer e o inflector para processar as palavras
stemmer = SnowballStemmer('portuguese')
inflector = inflect.engine()

# Definir o dicionário de termos e postings
terms_dict = {}

# Iterar pelos arquivos PDF na pasta
for filename in os.listdir('Docs'):
    if filename.endswith('.pdf'):
        # Abrir o arquivo PDF e extrair o texto
        with open(os.path.join('Docs', filename), 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()

        # Usar expressões regulares para encontrar todas as palavras no texto
        words = re.findall(r'\b\w+\b', text.lower(), re.UNICODE)

        # Remover stopwords
        words = [word for word in words if word not in stop_words]

        # Lematizacao nao aceita portugues
        # words = [lemmatizer.lemmatize(word) for word in words]
        nlp = spacy.load('pt_core_news_sm')
        words = [token.lemma_ for token in nlp(' '.join(words))]

        # Processar as palavras
        words = [inflector.singular_noun(
            stemmer.stem(word)) or word for word in words]

        # Iterar pelas palavras e adicionar as entradas apropriadas ao dicionário de termos e postings
        for word in words:
            if word in stop_words:
                continue #pula a iteração atual do loop se a palavra atual for uma stopword.
            if word in terms_dict:
                if filename in [docid for docid, freq in terms_dict[word]]:
                    for posting in terms_dict[word]:
                        if posting[0] == filename:
                            posting[1] += 1
                else:
                    terms_dict[word].append([filename, 1])
            else:
                terms_dict[word] = [[filename, 1]]

# Iterar pelo dicionário de termos e postings e imprimir os termos seguidos do nome do arquivo e da frequência com Pandas
index_data = []
for term, postings in sorted(terms_dict.items()):
    freq = sum([freq for filename, freq in postings])
    postings_list = ', '.join(
        [f'({docid}, {freq})' for docid, freq in postings])
    index_data.append({'Termo': term, 'Freq': freq, 'Postings': postings_list})


# Define um dataframe Pandas para a criação das tabelas
index_df = pd.DataFrame(index_data)
print(index_df)

# Salvar o Indice Invertido em um relatorio txt
file_path = 'Relatorios/Relatorio_Indice_Invertido2.txt'

# Verificar se o arquivo ainda não existe
if not os.path.exists(file_path):
    with open(file_path, 'w+') as f:
        f.write('❶ Índice Invertido ❶\n\n')

# Salvar Índice Invertido no relatório
with open('Relatorios/Relatorio_Indice_Invertido2.txt', 'a') as arquivo_saida:
    for term, postings in terms_dict.items():
        freq = len(postings)
        arquivo_saida.write(
            'Termo "{}" encontrado em {} documento(s):\n {}\n\n'.format(term, freq, postings))

# Salvar as Stopwords em um relatorio txt
file_path = 'Relatorios/Relatorio_Stopwords2.txt'
# Verificar se o arquivo ainda não existe
if not os.path.exists(file_path):
    with open(file_path, 'w+') as f:
        f.write('❶ Stopwords ❶\n\n')

# Salvando Stopwords no relatorio
with open('Relatorios/Relatorio_Stopwords2.txt', 'a') as f:
    for word in stop_words:
        f.write(word + '\n')

# Salvar a lematização em um arquivo de texto
with open('lemmatization.txt', 'w') as f:
    f.write('\n'.join(words))

# Salvar o índice invertido em um relatorio XLSX
index_df.to_excel(
    'Relatorios/Relatorio_Indice_Invertido_Tabela.xlsx', index=False)
