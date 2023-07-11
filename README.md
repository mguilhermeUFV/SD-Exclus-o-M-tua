## Instalando o Python 3 no Ubuntu

Para instalar o Python 3 no Ubuntu, siga as instruções abaixo:

1. Abra o Terminal do Ubuntu.
2. Atualize o gerenciador de pacotes com o comando:
3. Instale o Python 3 com o seguinte comando:
```bash
sudo apt install python3
```
4. Verifique se a instalação foi bem-sucedida executando o seguinte comando:
```bash
python3 --version
```
O comando deve exibir a versão do Python 3 instalada no seu sistema.

## Criando os arquivos "criador_de_processos.py" e "coordenador_de_regiao_critica.py"
1. Abra o Terminal do Ubuntu.
2. Navegue até o diretório onde você deseja criar os arquivos usando o comando cd. Por exemplo, para navegar até a pasta "MeusDocumentos", execute o seguinte comando:
```bash
cd MeusDocumentos
```
3. Crie o arquivo "criador_de_processos.py" utilizando o comando touch:
```bash
touch criador_de_processos.py
```
4. Abra o arquivo "criador_de_processos.py" com o editor de texto de sua preferência e cole o código disponibilizado no arquivo.
5. Repita os passos 3 e 4 para criar e editar o arquivo "coordenador_de_regiao_critica.py".

## Executando os arquivos com o Python 3
1. Abra o Terminal do Ubuntu.
2. Navegue até o diretório onde os arquivos "criador_de_processos.py" e "coordenador_de_regiao_critica.py" estão localizados usando o comando cd. Por exemplo, se os arquivos estiverem na pasta "MeusDocumentos", execute o seguinte comando:
```bash
cd MeusDocumentos
```
Execute o arquivo "criador_de_processos.py" com o seguinte comando:
```bash
sudo python3 criador_de_processos.py
```
Execute o arquivo "coordenador_de_regiao_critica.py" com o seguinte comando:
```bash
sudo python3 coordenador_de_regiao_critica.py
```

Certifique-se de executar primeiro o arquivo "coordenador_de_regiao_critica.py" na máquina coordenador e, em seguida, o arquivo "criador_de_processos.py" na maquina do processo. Também é importante alterar o indereço de IP e porta para atender as suas necessidades.