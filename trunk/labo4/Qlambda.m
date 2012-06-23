function [Q, reward_episode]=Qlambda(mdp)

% Inicializar Q a valores arbitrarios
Q=zeros(mdp.num_states,mdp.num_actions);
e=zeros(mdp.num_states,mdp.num_actions);

num_episodios=1000;
alpha=0.1;
max_steps=100;
lambda = 0.9;

reward_episode = zeros(1,num_episodios);
for episodio=1:num_episodios
    s=randi(mdp.num_states);
    steps=1;
    eoe=false;    
    a=chooseAction(Q,s);
    
    while(~eoe && steps<max_steps)
       [s_next,r,eoe]=mdp.simularAmbiente(s,a);
       
       a_next = chooseAction(Q,s_next);
       exploit = Q(s_next,a_next)==max(Q(s_next,:));
       
       delta = r + mdp.gamma * max(Q(s_next,:)) - Q(s,a);
       
       e(s,a) = e(s,a) +1;
       
       for i=1:mdp.num_states
           for j=1:mdp.num_actions
               Q(i,j) = Q(i,j) + alpha * delta * e(i,j);
               
               if exploit
                   e(i,j) = mdp.gamma * lambda * e(i,j);
               else
                   e(i,j) = 0;
               end                
           end
       end       

       reward_episode(episodio) = reward_episode(episodio) + r;
       a = a_next;
       s=s_next;
    end
end
