classdef cTDupdate
    properties
        alpha;
    end
    
    methods
        function obj = cTDupdate(init_alpha)
            obj.alpha=init_alpha;
        end
        
        function [Q] = update(obj, Q, arm, obs_pay)
            % Escribir funcion que actualiza valor Q del brazo arm en base
            % a la observacion recibida.
            delta = obs_pay - Q(arm);
            Q(arm) = Q(arm) + (obj.alpha * delta);
        end
    end
    
end


