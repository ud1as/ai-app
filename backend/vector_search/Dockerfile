FROM postgres:14

# Install dependencies and pgvector
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    postgresql-server-dev-14 \
    && wget https://github.com/pgvector/pgvector/archive/refs/tags/v0.5.1.tar.gz \
    && tar -xzf v0.5.1.tar.gz \
    && cd pgvector-0.5.1 \
    && make \
    && make install \
    && cd .. \
    && rm -rf pgvector-0.5.1 v0.5.1.tar.gz \
    && apt-get remove -y wget build-essential \
    && apt-get autoremove -y \
    && apt-get clean

CMD ["postgres"]
