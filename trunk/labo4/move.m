function [S_res] = move(S, action)
% action is 'N', 'O', 'S', 'E'.
    S_res = S;
    moved = false;
    switch action
        case {'N'}
            if S_res.y>1
                S_res.y = S_res.y - 1;
                moved = true;
            end
        case {'S'}     
            if S_res.y<5
                S_res.y = S_res.y + 1;
                moved = true;
            end
        case {'O'} 
            if S_res.x>1
                S_res.x = S_res.x - 1;
                moved = true;
            end    
        case {'E'}
            if S_res.x<5
                S_res.x = S_res.x + 1;
                moved = true;
            end
    end
    if moved
        if forbiddenMove(S, S_res)
            S_res = S;
        end
    end
end

