function [Q]=Qlearning(mdp)

% Inicializar Q a valores arbitrarios
Q=zeros(mdp.num_states,mdp.num_actions);

num_episodios=100;
alpha=0.1;
max_steps=50;

for e=1:num_episodios
    s=1;
    steps=1;
    while(~eoe(mdp,s) && steps<max_steps)
        %% COMPLETAR
        % Elegir una accion
        a = chooseAction(Q, s);
        % Tomar la accion y observar el resultado (s' y r)
        [s_next, r] = simularAmbiente(mdp,s,a);
        % Actualizar Q
        Q(s,a) = Q(s,a) + alpha * ( r + (mdp.gamma * max(Q(s_next,:))) - Q(s,a));
        % Actualizar el estado actual s
        s = s_next;
        steps=steps+1;
    end
end
