# Configurando o ambiente
Para instruções de como instalar o Docker e o Docker-compose clique [aqui](https://github.com/Kalkuli/2018.2-Kalkuli_Front-End/blob/master/README.md).


<br>

## Colocando no ar
Com o Docker e Docker-Compose instalados, basta apenas utilizar os comandos:

> ```chmod +x entrypoint.sh```

> ```docker-compose -f docker-compose-dev.yml up --build```

Acesse o servidor local no endereço apresentado abaixo:

http://localhost:5003/


Agora você já pode começar a contribuir!




<br>

## Outros comando importantes para desenvolvimento

* Recriar o banco de dados local:

> ```docker-compose -f docker-compose-dev.yml run base python manage.py recreatedb```

* Acessar o banco de dados local:

> ```docker-compose -f docker-compose-dev.yml exec db psql -U postgres```