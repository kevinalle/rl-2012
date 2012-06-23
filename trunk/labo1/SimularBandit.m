function [ rewards choice ] = SimularBandit( kProbs, Qinit, fActionSelection, fValueUpdate, ntrials )
% Función que simula un bandido de k-brazos, donde cada brazo tiene
% probabilidad de "pagar" según kProbs. El brazo es elegido por la función
% fActionSelection y el valor actualizado por fValueUpdate.

    k=length(kProbs);
    
    rewards = zeros(1,ntrials);
    choice = zeros(1,ntrials);
    
    Q = Qinit;
    for t = 1:ntrials
        % Elegir brazo
        arm=fActionSelection(Q);
        choice(1,t)=arm;
        
        % Observar resultado
        obs_pay = (rand()<kProbs(arm));
        rewards(1,t)=obs_pay;

        % Actualizar valor
        Q=fValueUpdate(Q,arm,obs_pay);
    end
    
end

