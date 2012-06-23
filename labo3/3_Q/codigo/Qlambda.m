function [Q, reward_episode]=Qlambda(mdp)

% Inicializar Q a valores arbitrarios
Q=zeros(mdp.num_states,mdp.num_actions);
e=zeros(mdp.num_states,mdp.num_actions);

num_episodios=500;
alpha=0.1;
max_steps=100;
lambda = 0.9;

reward_episode = zeros(1,num_episodios);
for episodio=1:num_episodios
    s=randi(mdp.num_states);
    steps=1;
    eoe=false;    
    while(~eoe && steps<max_steps)
        a=chooseAction(Q,s);
        [s_next,r,eoe]=mdp.simularAmbiente(s,a);
        [val best_a] = max(Q(s_next,:));
        delta = (r + mdp.gamma * max(Q(s_next,:)) - Q(s,a));
        e(s, a) = e(s, a) + 1;
        for i_s = 1:mdp.num_states
            for i_a = 1:mdp.num_actions
                Q(i_s, i_a) = Q(i_s, i_a) + alpha*delta*e(i_s, i_a);
                if (best_a == a)
                    e(i_s, i_a) = mdp.gamma*lambda*e(i_s, i_a);
                else
                    e(i_s, i_a) = 0;
                end
            end
        end
        s=s_next;
        steps=steps+1;
    end
end
