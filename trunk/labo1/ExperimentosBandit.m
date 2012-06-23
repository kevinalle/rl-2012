bandit = [0.6 0.8 0.1 0.5];
trials = 100;
reps=2;

% Epsilon greedy
epsilons=[0.1 0.3 1];
oUpdate=cTDupdate(0.1);
oAction=cEpsilonGreedy(0);
Qinit=zeros(length(bandit),1);
[xxx, arms]=correrExperimento(bandit, Qinit, oAction, oUpdate, reps, trials, epsilons);
graficarSeleccionArms(arms);
title('Epsilon Greedy'); xlabel('Epsilon');
set(gca,'XTick',1:length(epsilons));
set(gca,'XTickLabel', cellfun(@num2str,num2cell(epsilons), 'UniformOutput', false));

% Epsilon greedy con optimistic initialization
epsilons=[0.1 0.3 1];
oUpdate=cTDupdate(0.1);
oAction=cEpsilonGreedy(0);
Qinit=ones(length(bandit),1);
[xxx, arms]=correrExperimento(bandit, Qinit, oAction, oUpdate, reps, trials, epsilons);
graficarSeleccionArms(arms);
title('Epsilon Greedy Optimistic Init'); xlabel('Epsilon');
set(gca,'XTick',1:length(epsilons));
set(gca,'XTickLabel', cellfun(@num2str,num2cell(epsilons), 'UniformOutput', false));

% Softmax
betas=[0.5 1 2 10];
oUpdate=cTDupdate(0.1);
oAction=cSoftmax(0);
[xxx, arms]=correrExperimento(bandit, Qinit, oAction, oUpdate, reps, trials, betas);
graficarSeleccionArms(arms);
title('Softmax'); xlabel('Beta');
set(gca,'XTick',1:length(betas));
set(gca,'XTickLabel', cellfun(@num2str,num2cell(betas), 'UniformOutput', false));
