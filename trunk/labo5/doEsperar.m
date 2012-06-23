function [s_next]=doEsperar(s)

padres=[ 2 3 ; 1 4 ; 1 2 ; 5 6 ; 2 3 ; 1 2 ]; %original
% padres=[ 2 6 ; 6 5 ; 1 2 ; 2 6 ; 3 4 ; 1 2 ]; %rotacion 1
% padres=[ 5 6 ; 1 3 ; 4 6 ; 5 6 ; 4 6 ; 2 5 ];  %rotacion 2
n=length(padres);

s_next=zeros(1,n);
for i=1:n
    prob=0.5*s(i) + sum(0.15*s(padres(i,:))) + 0.1;
%     prob=0.15*s(i) + 0.50*s(padres(i,1)) + 0.15*s(padres(i,2)) + 0.1;
   s_next(i)=(rand()<prob);
end