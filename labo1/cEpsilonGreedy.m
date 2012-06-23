classdef cEpsilonGreedy
    properties
        epsilon;
    end
    
    methods
        function obj = cEpsilonGreedy(init_epsilon)
            obj.epsilon=init_epsilon;
        end
        
        function [obj] = setParam(obj,param)
            obj.epsilon=param;
        end
        
        function [arm] = getArm(obj,Q)
            % Escribir codigo que devuelva un numero de brazo segun el
            % criterio epsilon-greedy. 
            % En caso de empate entre dos o mas valores, elegir al azar.
            if rand(1) < obj.epsilon
                [val, arm] = max(Q);
            else
                dim = size(Q);
                arm = randi(dim(1));
            end
        end
        
    end
    
end
