# Automacao-LumikitSHOW-SL1000

# Introdução

Algoritmo projetado para facilitar a abertura do aplicativo LumikitSHOW utilizando a interface USB SL1000, ele realiza a criação de uma janela de carregamento e a abertura dos apps necessários para a utilização correta do LumikitSHOW.

É necessário a abertura de um software do FreeStyle para a utilização da interface SL1000 no LumikitSHOW, o Art-Net, isso se dá porque o LumikitSHOW não utiliza mais, desde 2011, interfaces USB para DMX mas sim apenas Ethernet para DMX.

Esse algoritmo foi projetado para ser inicializado logo após inicializar o computador, utilizando o agendador de tarefas do Windows, sendo explicado como configurar essa tarefa no tópico 'Agendador de Tarefas'.

A janela de carregamento foi projetada para que o usuário possa ter a certeza de que o software da automação de fato está em andamento e evitando que seja aberto mais de uma vez manualmente, isso pois ficará cerca de dois minutos em espera, projetado dessa maneira por conta do computador utilizado por este aplicativo, tratasse de um notebook antigo e lento, utilizando Windows 8.1, levando aproximadamente esse tempo para sua inicialização correta do sistema operacional. Para alterar esse tempo de espera e demais constantes consulte o tópico 'Requisitos'.

# Procedimentos

# Funcionamento

Ele irá realizar os seguintes procedimentos:

- Criar a janela de carregamento, com o intuito de prevenir erros na abertura se tratar-se de um computador antigo; 
- Inicializar o programa Art-Net, do software de iluminação FreeStyle com a interface pré-configurada;
- Inicializar o programa LumikitACAP, utilizado para detecção automática do tempo da música atual do evento, já configurando o microfone;
- Inicializar o programa LumikitSHOW, com a interface pré-configurada.

# Agendador de Tarefas
