classdef cSoftmax
    properties
        beta;
    end
    
    methods
        function obj = cSoftmax(init_beta)
            obj.beta=init_beta;
        end

        function [obj] = setParam(obj,param)
            obj.beta=param;
        end
        
        function [arm] = getArm(obj,Q)
            % Escribir la funcion que devuelva un brazo en base a la regla
            % softmax.
            terms = exp(obj.beta*Q);
            suma = sum(terms);
            real_terms = terms / suma;
            dim = size(Q);
            res = zeros(dim);
            for i = [1:dim]
                res(i) = sum(real_terms(1:i));
            end
            r = rand(1);
            arm = 1;
            while r > res(arm)
                arm = arm + 1;
            end
            
        end
        
    end
    
end
