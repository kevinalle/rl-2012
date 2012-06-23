disp('Cargando MDP Taxi');
load('MDPTaxi.mat');

disp('Corriendo Qlearning');
[Q rew_epi]=Qlearning(mdp);

plot(tsmovavg(rew_epi,'s',20));