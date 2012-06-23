function [a]=chooseAction(Q,s)
    epsilon=0.1;
    
    if(rand()<epsilon)
        a=randi(size(Q,2));
    else
        % Romper empates
        as=find(Q(s,:)==max(Q(s,:)));
        a=as(randi(length(as)));
    end
