function [s_next,r] = simularAmbiente(mdp,s,a)

    probs=mdp.T(s,:,a);
    s_next=mnrnd(1,probs)*(1:mdp.num_states)';
    
    if(eoe(mdp,s_next))
        r=1;
    else
        r=mdp.R(s,a);
    end