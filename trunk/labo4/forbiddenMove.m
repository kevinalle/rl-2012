function [ res ] = forbiddenMove( pos1, pos2 )
%pos1 y pos2 deben ser casilleros adyacentes
    res = false;
    if pos1.x==pos2.x %movimiento vertical, todos permitidos
       res = false; 
    else%movimiento horizontal
        if pos1.x>=pos2.x
            pos1 = pos2;
        end
        if pos1.x == 1
            res = pos1.y>=4;
        elseif pos1.x == 2
            res = pos1.y<=2;
        elseif pos1.x == 3
            res = pos1.y>=4;
        end            
    end
end

