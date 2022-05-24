# SRV - Software de reprodu��o de voltas

 O objetivo principal do presente trabalho � minimizar os fatores de interfer�ncia durante as voltas de teste de diferentes ajustes. Atrav�s de um sistema de controle capaz de realizar repetidas voltas sobre o mesmo tra�ado em um simulador, o fator humano ser� removido, passando a responsabilidade de replicar voltas para o algoritmo proposto. Abaixo do objetivo principal est�o os objetivos secund�rios de avaliar a diferen�a de tempo de volta utilizando diferentes configura��es de aerodin�mica, freio ou suspens�o, assim como segmentar o software para que seja poss�vel alterar o modelo controlador e adaptar para diferentes simuladores.
 
 
 ## Instala��o e configura��o
 
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
 

 ## Doumenta��o
   
  [Link da biblioteca de componente visual](https://realpython.com/python-gui-with-wxpython/)
  
  [Link da biblioteca do controle virtual](https://pypi.org/project/vgamepad/)
  
  [Link da biblioteca de telemetria F1 2021](https://github.com/chrishannam/Telemetry-F1-2021)
  
  [Link do software de telemetria do jogo F1 2021](https://bitbucket.org/Fiingon/pxg-f1-telemetry/downloads/)
