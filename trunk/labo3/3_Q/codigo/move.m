function [S_res] = move(S, action)
% action es 'N', 'O', 'S', 'E'.
% Chequear si se choco con pared usando forbiddenMove.m
curr_pos = struct();
curr_pos.x = S.x;
curr_pos.y = S.y;
next_pos = curr_pos;
next_pos.y = S.y;
next_pos.x = S.x;

if action == 'O'
    next_pos.x = S.x - 1;
elseif action == 'E'
    next_pos.x = S.x + 1;
end

if action == 'N'
    next_pos.y = S.y - 1;
elseif action == 'S'
    next_pos.y = S.y + 1;
end


S_res = S;
if ~forbiddenMove(curr_pos, next_pos)
    S_res.x = next_pos.x;
    S_res.y = next_pos.y;
end

