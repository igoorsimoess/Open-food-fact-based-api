## The Project

API para retornar dados relevantes do Open Food Facts a fim de facilitar a obtenção desses dados para a Fitness Foods LC.

API that returns relevant data from Open Food Facts in order to retrieve nutritional data for Fitness Foods LC.

### How to run the project:

##### clone the repository
``` 
git clone <this repository>
```
##### Go to api root directory and run:

```
cd food_details_api && docker-compose up
```

##### Perform a consult:

Open any client service like Insomnia or Postman and perform a request to localhost on port 5000.

Available endpoints:

```
http::/127.0.0.1:8000/ - for info about the API
http::/127.0.0.1:8000/products - to list all paginated db
http::/127.0.0.1:8000/products/<code> - to retrieve one updated product db

```

### How to test the endpoints
##### API up:

```
cd /food_details/tests/ && pytest tests.py

```

### Docs

Swagger/OpenAPI was configured in order to provide a better view for the API resources. 

```
127.0.0.1:8000/swagger/

```

#### Some cool features
##### Portuguese 

- Todo o projeto está em uma imagem docker e usa docker-compose para assegurar a conexão com o postgres.
- Na intenção de sempre ter os dados mais atualizados sobre um produto de acordo com a base do OpenFoodFacts, 
ao fazer um requisição get para um produto específico, a API da OpenFoodFacts é consultada e os dados são atualizados na hora,
tanto na view quanto no db.

        - Essa abordagem foi escolhida dado o cenário inicial - em que se tinha um dataset csv com dados faltantes - a 
        consulta a todos as mais de 5000 entradas de dados não seria performática. Melhor fazer uma requisição inplace a cada produto.

- A importação dos dados, criação da base de dados e tabela, população da tabela e tratamento de dados é feita de forma automatizada 
via script bash + python 

- Também foi criado um script bash que garante que a conexão com o banco de dados foi feita, rodando migrações e server de forma automática. 