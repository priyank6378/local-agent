FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3 curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"
ENV OLLAMA_HOST=http://host.docker.internal:11434

WORKDIR /app/priyank/fast_api_agent

COPY pyproject.toml /app/priyank/fast_api_agent

RUN uv sync

COPY fast_api_agent ./

CMD [ "uv", "run" , "fastapi", "run", "api_endpoints.py" ]