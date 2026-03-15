# 1. Use an official, lightweight Python Linux image
FROM python:3.10-slim

# 2. Install curl and zstd (needed to download and extract Ollama)
RUN apt-get update && apt-get install -y curl zstd

# 3. Install Ollama into the Linux container
RUN curl -fsSL https://ollama.com/install.sh | sh

# 4. Set the working directory inside the container
WORKDIR /app

# 5. Copy your requirements file and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy all your code (main.py, index.html) into the container
COPY . .

# 7. BIG TRICK: Start Ollama in the background and bake your GGUF model directly into the image!
# This ensures Google Cloud doesn't have to download the model every time someone visits the site.
RUN nohup bash -c "ollama serve &" && sleep 5 && ollama pull hf.co/MalinZZZRayWed/Llama-3-Resume-Parser-GGUF

# 8. Expose port 8080 (This is the mandatory port for Google Cloud Run)
EXPOSE 8080

# 9. Create a startup script that runs both Ollama AND your FastAPI app at the same time
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 5\n\
uvicorn main:app --host 0.0.0.0 --port 8080\n\
' > start.sh
RUN chmod +x start.sh

# 10. Command to run when the cloud server wakes up
CMD ["./start.sh"]