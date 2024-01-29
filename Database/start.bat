docker build -t postgresdb .

docker run --name postgresdb -d -p 9100:5432 postgresdb 

