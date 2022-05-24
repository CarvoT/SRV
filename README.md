# SRV - Software de reprodução de voltas

 O objetivo principal do presente trabalho é minimizar os fatores de interferência durante as voltas de teste de diferentes ajustes. Através de um sistema de controle capaz de realizar repetidas voltas sobre o mesmo traçado em um simulador, o fator humano será removido, passando a responsabilidade de replicar voltas para o algoritmo proposto. Abaixo do objetivo principal estão os objetivos secundários de avaliar a diferença de tempo de volta utilizando diferentes configurações de aerodinâmica, freio ou suspensão, assim como segmentar o software para que seja possível alterar o modelo controlador e adaptar para diferentes simuladores.
 
 
 ## Instalação e configuração
 
 ### Visual Studio
 
 O projeto foi desenvolvido dentro do Visual Studio e todos comandos foram feitos no console do VS.
 
 #### Pacote python
 
 Utilizar o Visual Studio Instaler para instalar o pacote de desenvolvimento em pyhon
 ![image](https://user-images.githubusercontent.com/73369063/148464219-d3dddda2-87c2-44b2-8569-96e451239241.png)
 
 #### Biblioteca controle
 > pip install vgamepad
 
 #### Biblioteca GUI
  > pip install wxpython

 #### Biblioteca F1 2021 telemetria
 > pip install Telemetry-F1-2021
 

 ## Doumentação
   
  [Link da biblioteca de componente visual](https://realpython.com/python-gui-with-wxpython/)
  
  [Link da biblioteca do controle virtual](https://pypi.org/project/vgamepad/)
  
  [Link da biblioteca de telemetria F1 2021](https://github.com/chrishannam/Telemetry-F1-2021)
  
  [Link do software de telemetria do jogo F1 2021](https://bitbucket.org/Fiingon/pxg-f1-telemetry/downloads/)
