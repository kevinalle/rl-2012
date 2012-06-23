function [V,policy] = VI(mdp)

nS=mdp.num_states;
nA=mdp.num_actions;
epsilon=0.001;

% Inicializar V y Q a valores arbitrarios
Q=zeros(nS,nA);
V=zeros(nS,1);
stop=false;

% Ciclar hasta que entre una iteracion y otra haya poco (<epsilon) cambio
% en los valores.
while(~stop)
    delta=0;
    % Para cada estado, para cada accion...
    for s=1:nS
        for a=1:nA
            % Guardar Q actual para luego compararlo con el actualizado y
            % medir cuanto cambio (para saber cuando parar el ciclo
            % principal)
            q=Q(s,a);

            % Actualizar Q
            Q(s,a) = mdp.R(s,a) + mdp.gamma * mdp.T(s,:,a) * V;
            

            % Medir el cambio maximo en Q
            delta = max(delta, abs(q - Q(s,a)));
            
            % Calcular V como el Q maximo para cada estado
            V = max(Q')';
            
        end
    end
    % Si delta<epsilon, parar
    stop=(delta<epsilon);
end

% Extraer el policy de Q
[p,policy]=max(Q,[],2);
