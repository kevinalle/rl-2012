function [rews arms] = correrExperimento(bandit, Qinit, oAction, oUpdate, reps, trials, params)

nparams=length(params);
rews=zeros(nparams,reps,trials);
arms=zeros(nparams,reps,trials);
for i=1:nparams
    oAction=oAction.setParam(params(i));
    for r=1:reps
        [rews(i,r,:) arms(i,r,:)]=SimularBandit(bandit, Qinit, @oAction.getArm, @oUpdate.update, trials);
    end
end
