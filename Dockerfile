# 1. Imagem base oficial leve do Python
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o resto do código da aplicação para o contêiner
COPY . .

# 5. Expõe a porta que o Flask utiliza
EXPOSE 5000

# 6. Comando para iniciar a aplicação
CMD ["python", "app.py"]