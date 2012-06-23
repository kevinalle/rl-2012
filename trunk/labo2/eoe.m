function [end_of_episode]=eoe(mdp,s)
    end_of_episode=~isempty(find(mdp.EOE==s, 1));