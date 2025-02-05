#!/usr/bin/env python
import sys

import click

from gym_tictactoe.env import TicTacToeEnv, agent_by_mark, check_game_status,\
    after_action_state, tomark, next_mark

switch=1
class HumanAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(self, state, ava_actions):
        while True:
            uloc = input("Enter location[1-9], q for quit: ")
            if uloc.lower() == 'q':
                return None
            try:
                action = int(uloc) - 1
                if action not in ava_actions:
                    raise ValueError()
            except ValueError:
                print("Illegal location: '{}'".format(uloc))
            else:
                break

        return action

class MinimaxAgent(object):
    def __init__(self, mark):
        self.mark = mark


#   return the move in this function. ava_actions is an array containting the possible actions 
#   you might want to use after_action_state and check_game_status. Also look at env.py
#   state is a tuple with the first value indicating the board and second value indicating mark
#   proper use of inbuilt functions will avoid interacting with state
    def act(self, state, ava_actions):
        board,mark=state
        nboard = list(board[:])
        if check_game_status(nboard)<0:
            min=100
            max=-100
            action_min=ava_actions[0]
            action_max=ava_actions[0]
            if mark=='O':
                for action in ava_actions:
                    nboard[action]=1
                    mark=next_mark(mark)
                    value , q =self.act((tuple(nboard),mark),[p for p in ava_actions if p!=action])
                    if (value < min):
                        min = value
                        action_min = action
                    nboard[action]=0        #backtrack
                    mark=next_mark(mark)
                return min,action_min
            else:
                for action in ava_actions:
                    nboard[action]=2
                    mark=next_mark(mark)
                    value,m =self.act((tuple(nboard),mark),[p for p in ava_actions if p!=action])
                    if (value > max):
                        max = value
                        action_max = action
                    nboard[action]=0        #backtrack
                    mark=next_mark(mark)
                return max,action_max
        else:
            return check_game_status(nboard),12








        #raise NotImplementedError()

@click.command(help="Play minimax agent.")
@click.option('-n', '--show-number', is_flag=True, default=False,
              show_default=True, help="Show location number in the board.")
def play(show_number):
    env = TicTacToeEnv(show_number=show_number)
    agents = [MinimaxAgent('O'),
              HumanAgent('X')]
    episode = 0
    while True:
        state = env.reset()
        _, mark = state
        done = False
        env.render()
        while not done:
            agent = agent_by_mark(agents, mark)
            env.show_turn(True, mark)
            ava_actions = env.available_actions()
            if mark=='O':
                n , action = agent.act(state, ava_actions)
            else:
                action = agent.act(state, ava_actions)
            if action is None:
                sys.exit()

            state, reward, done, info = env.step(action)
        
            print('')
            env.render()
            if done:
                env.show_result(True, mark, reward)
                break
            else:
                _, _ = state
            mark = next_mark(mark)

        episode += 1


if __name__ == '__main__':
    play()
