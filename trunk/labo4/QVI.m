function [Q] = QVI(T,R,C, mdp, M, Vmax)

nS=mdp.num_states;
nA=mdp.num_actions;
epsilon=0.01;

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

            % Actualizar Q: si la cuenta de visitas (s,a) es menor que M, Q
            % es Vmax. Si no, calcular usando el modelo.
            if C(s,a) < M
                Q(s,a) = Vmax;
            else
                residuo = mdp.gamma * (squeeze(T(s,a,:))'/C(s,a)) * V;
                Q(s,a) = R(s,a)/C(s,a) + residuo;
            end
            
            % Medir el cambio maximo en Q
            delta=max([delta abs(q-Q(s,a))]);
            
            % Calcular V como el Q maximo para cada estado
            V=max(Q,[],2);
            
        end
    end
    % Si delta<epsilon, parar
    stop=(delta<epsilon);
end
