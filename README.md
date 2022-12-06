# Projeto Final Redes de Computadores: Chat Room

### *Projeto desenvolvido para avaliação final da matéria de Redes de Computadores* 

## Inicializando a aplicação
Primeiro o código ```server_v2.py``` deve ser executado com o comando ```python server_v2.py``` no terminal. Após isso, o código ```client_w_gui.py``` deve ser executado com o comando ```python client_w_gui.py``` no terminal. Ao ser executado, uma janela aparecerá pedindo um apelido, que identificará o cliente na sala. Vários clientes podem utilizar a sala ao mesmo tempo.

### Admin

Ao definir seu apelido como ***admin***, tal cliente pode utilizar dos comandos ```/ban``` ou ```/kick``` seguido pelo apelido do cliente que você deseja remover da sala.

## Aplicação

São usadas as bibliotecas ***socket*** (para as funções de envio e recebimento dos dados através da rede), ***threading*** (para as funções de ocorrências simultâneas no programa) e ***tkinter*** (para a criação da interface visual do chat).

São necessários dois códigos na realização do projeto: inicialmente, deve ser inicializado o servidor, que é um *socket* aberto que recebe constantemente as mensagens e as reenvia para todos os usuários (broadcast) que estiverem dentro de uma sala criada específica; o segundo código identifica a parte do socket remoto por parte do cliente, que serve para o recebimento das mensagens e a formação de uma interface visual para o chat, que é feita a partir das funcionalidades na biblioteca *tkinter*.

### Thread
O *Thread*, como complementar, é usado para controlar o fluxo de mensagens que são enviadas e recebidas pelo cliente, tornando possíveis as conexões TCP concorrentes no programa, para que o chat funcione simultaneamente entre os clientes no mesmo servidor, possibilitando o fluxo de controle sequencial dentro do programa.

### Módulo Socket

```socket.socket(family = , type = )``` inicia uma conexão, deixando um socket em aberto e definindo a conexão. Para a criação de um socket, é necessária a passagem de parâmetros do endereço da família e do tipo de socket. Foram usados AF_INET para indicar o uso da família de endereços para IPV4 e o tipo SOCK_STREAM, que é utilizado na implementação da conexão TCP.

```socket.bind(address)```, usado no código server, recebe os parâmetros de HOST e PORT em tupla como o endereço no parâmetro e os liga com o socket, identificando onde será realizado, necessitando que o endereço não esteja ligado a outro socket previamente. De forma semelhante, em client, é usado ```socket.connect(address)``` para conectar o endereço em tupla com os mesmos HOST e PORT já estabelecidos pelo bind em um socket remoto. Com isso, é feita a conexão inicial entre o servidor e o client.

```socket.listen()``` define o limite das conexões, permitindo ao servidor a realização das conexões possíveis, para processar o dado quando chegarem as informações. Tipicamente o servidor se mantém em um laço infinito para receber novas conexões. ```socket.accept()``` é o objeto que permite ao servidor aceitar a conexão.

```recv``` é usado para o recebimento de dados do socket, enquanto send é o objeto usado para o envio deles, ambos operando nos buffers de rede. Ambos são utilizados com encode e decode quando é necessária a conversão dos conteúdos dos dados enviados. É no par de recebimento e envio de mensagens que há a comunicação lógica no processo.

```socket.bind(address)```, usado no código server, recebe os parâmetros de HOST e PORT em tupla como o endereço no parâmetro e os liga com o socket, identificando onde será realizado, necessitando que o endereço não esteja ligado a outro socket previamente. De forma semelhante, em client, é usado ```socket.connect(address)``` para conectar o endereço em tupla com os mesmos HOST e PORT já estabelecidos pelo bind em um socket remoto. Com isso, é feita a conexão inicial entre o servidor e o client.
A estrutura do chat em grupo se dá pela separação de salas e a conexão de clientes nestas pelo login inicial, que os envia para a sala se já criada ou inicializa uma sala nova com o título indicado. A função intitulada ```broadcast``` é usada para enviar as mensagens para todos os usuários conectados em determinada sala, recebendo o conteúdo das mensagens enviadas pelo client, e em seguida enviando para todos os outros à partir do servidor.
