# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import game_logic

board = game_logic.initial_board()
current_player = game_logic.BLACK

@api_view(['GET', 'POST'])
def play_game(request):
    global board, current_player

    if request.method == 'GET':
        # Initialize the board and player on the first GET request
        LegalMoves=game_logic.legal_moves(current_player, board)
        return Response({'board': board, 'current_player': 'Black','legal_move':LegalMoves})

    elif request.method == 'POST':
        move = request.data.get('move')

        if not move:
            return Response({'error': 'Move not provided'}, status=400)

        player = current_player
        try:
            game_logic.make_move(move, player, board)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        black_score, white_score = game_logic.score(player, board)
        current_player = game_logic.next_player(board, player)

        # Make computer's move
        if current_player == game_logic.WHITE:
            move = game_logic.alphabeta_searcher(3, game_logic.weighted_score, board, current_player)
            game_logic.make_move(move, current_player, board)
            black_score, white_score = game_logic.score(current_player, board)
            current_player = game_logic.next_player(board, current_player)
        LegalMoves=game_logic.legal_moves(current_player, board)
        return Response({
            'board': board,
            'black_score': black_score,
            'white_score': white_score,
            'current_player': 'White' if current_player == game_logic.WHITE else 'Black',
            'legal_move':LegalMoves
        })
