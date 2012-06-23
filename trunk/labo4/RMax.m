function [Q, T, R, C, reward_episode]=RMax(mdp, M, rmax)

% Inicializar Q a valores arbitrarios
C=zeros(mdp.num_states,mdp.num_actions);
T=zeros(mdp.num_states,mdp.num_actions, mdp.num_states);
R=zeros(mdp.num_states,mdp.num_actions);
Vmax=rmax/(1-mdp.gamma);
Q=QVI(T,R,C,mdp,M,Vmax);

num_episodios=300;
alpha=0.1;
max_steps=25;

reward_episode = zeros(1,num_episodios);

for e=1:num_episodios
    s=randi(mdp.num_states);
    steps=1;
    eoe=false;
    disp(e);
    while(~eoe && steps<max_steps)
        % obtengo proxima accion de manera greedy
        [v, a] = max(Q(s,:));
        % simulo la accion y observo s', r y end-of-episode
        [s_next, r] = mdp.simularAmbiente(s, a);
        % actualizo estimaciones (modelo)
        T(s,a,s_next) = T(s,a,s_next) + 1.0;
        R(s,a) = R(s,a) + r;
        C(s,a) = C(s,a) + 1.0;
        % decido si correr QVI: solo si un par estado-accion paso de
        % unknown a known
        % actualizo Q
        if(C(s,a) == M+1)
            Q = QVI(T,R,C, mdp, M, Vmax);
        end
        
        % actualizo s y contadores
        s=s_next;
        reward_episode(e) = reward_episode(e) + r;
        steps=steps+1;
    end
    disp(reward_episode(e));
end
