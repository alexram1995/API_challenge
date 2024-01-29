FROM postgres:15.2-alpine

# Create a directory for initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy initialization scripts into the container
COPY initdb/*.sql /docker-entrypoint-initdb.d/

# Set environment variables for customization
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=postgres

# Expose the default PostgreSQL port
EXPOSE 5432
