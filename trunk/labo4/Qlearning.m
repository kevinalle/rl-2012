function [Q, reward_episode]=Qlearning(mdp)

% Inicializar Q a valores arbitrarios
Q=zeros(mdp.num_states,mdp.num_actions);

num_episodios=5000;
alpha=0.1;
max_steps=100;

reward_episode = zeros(1,num_episodios);
for e=1:num_episodios
    s=randi(mdp.num_states);
    steps=1;
    eoe=false;    
    while(~eoe && steps<max_steps)
       a=chooseAction(Q,s);
       [s_next,r,eoe]=mdp.simularAmbiente(s,a);
       reward_episode(e) = reward_episode(e) + r;
       Q(s,a)=Q(s,a)+alpha*(r + mdp.gamma * max(Q(s_next,:)) - Q(s,a));
       s=s_next;
       steps=steps+1;
    end
end
