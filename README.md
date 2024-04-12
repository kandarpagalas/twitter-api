# twitter-api

Este é um projeto desenvolvido para estudar `data mining`, `crawlers`,`web scraping` e `APIs`.
A escolha do Twitter foi motivada pela complexidade de realizar raspagem de dados em sua aplicação. Assim como a existencia de diversos pacotes para esta finalidade, o que demonstra a viabilidade do projeto.

## Recursos
twitter-api foi desenvolvido em de `Python` 3.11, com o uso de `Playwrite` e `FastApi`.

## Instalação
Siga os passos aseguir para rodar este projeto em um ambiente virtual. 
```bash
    # Clone o repositório
    git clone https://github.com/kandarpagalas/twitter-api.git
    # Cria o ambiente virtual
    python3 -m venv venv
    # Ativa o ambiente
    source venv/bin/activate
    # Instala o pacote que utilizamos para interagir com o navegador
    pip install pytest-playwright
    playwright install --with-deps
    # Instala as dependências do projeto
    pip install -r requirements
```

### Autenticação
Crie um arquivo de autenticação em `src/.session/` usando `autenticate.py`
```bash
    python src/autenticate.py
```

### Iniciar
```bash
    uvicorn src.main:app --host 0.0.0.0 --port 8000
```
* Você pode especificar a porta aoterando `8000`

## API
endpoint: [`http://0.0.0.0:8000`](http://0.0.0.0:8000)
documentação: [`http://0.0.0.0:8000/docs`](http://0.0.0.0:8000/docs)

## Deploy
#### headless
Para rodar em maquinas sem saída de vídeo, como o `ubuntu-server`, é necessário usar o `xvfb` para que o crawler funcione corretamente
```bash
    xvfb-run --auto-servernum uvicorn src.main:app --host 0.0.0.0 --port 8000
```
#### docker
Ainda não consegui viabilizar a criação de um container.


## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.