Agents: agent.py (best custom heuristic), other_agent.py (basic custom heuristic), randy_ai.py (random move selection)

Note: include flags -c -o for shorter AI turns. Additionally restrict -l <depth number> to a lower depth to reduce turn time.

$python3 othello_gui.py -d <dimension> [-a <agentA> -b <agentB> -l <depth-limit> -c -o -m]

Flag -m: agent uses MINIMAX algorithm. By default we don't need this flag because Alpha-beta pruning is enabled (which is an optimization of the base MINIMAX algorithm).
Flag -l <depth number>: depth limit for AI recursive computations. Greater depth allows for better AI strategy.
$python3 othello_gui.py -d <board size> -a agent.py -l 5
Flag -c: speeds up the AI by caching states we've seen before.
Flag -o: Toggle for node ordering. i.e., AI first explores nodes that lead to a better utility.



Can toggle AI vs AI by inputting both -a <agentA> and -b <agentB>
Can play against an AI player by inputting just  -a <agentA>