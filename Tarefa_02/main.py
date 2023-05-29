import os
import PyPDF2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

# Definir a lista de documentos
documents = []

# Iterar pelos arquivos PDF na pasta
for filename in os.listdir('Docs'):
    if filename.endswith('.pdf'):
        # Abrir o arquivo PDF e extrair o texto
        with open(os.path.join('Docs', filename), 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
        documents.append(text)

# Crie o vetorizador TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# Obtenha os termos
terms = vectorizer.get_feature_names()

# Converta a matriz X para uma matriz numpy
X = X.toarray()

# Normalize os vetores
X_normalized = normalize(X)

# Calcule as similaridades de cosseno entre os documentos
similarity_matrix = cosine_similarity(X_normalized)

# Obtenha os índices dos documentos ordenados por similaridade
document_indices = np.argsort(-similarity_matrix[0])

# Função para realizar a busca
def search(query):
    # Vetorizar a consulta
    query_vector = vectorizer.transform([query]).toarray()

    # Normalizar o vetor da consulta
    query_vector_normalized = normalize(query_vector)

    # Calcular as similaridades de cosseno entre a consulta e os documentos
    similarity_scores = cosine_similarity(query_vector_normalized, X_normalized)

    # Obter os índices dos documentos ordenados por similaridade
    document_indices = np.argsort(-similarity_scores[0])

   # Imprimir os resultados em uma janela estática
    for index in document_indices:
        document_index = document_indices[index]
        similarity = similarity_scores[0][document_index]
        print(f"Índice do documento: {document_index}")
        print(f"Similaridade de cosseno: {similarity}")
        print("---------")

# Realizar as buscas
print("----BUSCA----")
search("Busca1")
print("---------")
search("Busca2")
print("---------")
search("Busca3")
