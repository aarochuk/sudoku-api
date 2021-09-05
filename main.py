from flask import Flask, request, jsonify, render_template, url_for
from sudoku_gen import generate_board, string_board, list_board, _solve

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/new-board', methods=['GET'])
def new_board():
    # difficulty should be expressed as a number else it would return easy
    if request.args.get('diff'):
        difficulty = request.args.get('diff')
        if not difficulty.isdigit():
            difficulty = 1
        else:
            difficulty = int(difficulty)
            if difficulty > 3:
                difficulty = 3
            elif difficulty <= 0:
                difficulty = 1
    else:
        difficulty = 1

    if difficulty == 1:
        dif = 'easy'
    elif difficulty == 2:
        dif = 'medium'
    else:
        dif = 'hard'

    empty_board, solved_board = generate_board(difficulty)

    if request.args.get('stype'):
        if request.args.get('stype').lower() == 'string':
            empty_board = string_board(empty_board)
            solved_board = string_board(solved_board)
            print(empty_board)
            print(solved_board)

    if request.args.get('solu'):
        if request.args.get('solu').lower() == 'true':
            data = {
                'difficulty': dif,
                'unsolved-sudoku': empty_board,
                'solution': solved_board,
            }
        else:
            data = {
                'difficulty': dif,
                'unsolved-sudoku': empty_board,
            }
    else:
        data = {
            'difficulty': dif,
            'unsolved-sudoku': empty_board,
        }

    return jsonify(response=data), 200


@app.route('/verify-board')
def verify_board():
    if request.args.get('sudo'):
        if type(request.args.get('sudo')) == str and len(request.args.get('sudo')) == 81:
            board = list_board(request.args.get('sudo'))
            if _solve(board):
                return jsonify(response={
                    "board": request.args.get('sudo'),
                    "solvable": "True"
                }), 200
            else:
                return jsonify(response={
                    "board": request.args.get('sudo'),
                    "solvable": "False"
                }), 200
        else:
            return jsonify(response={
                "error": "Please input a board in the right format."
            }), 400
    else:
        return jsonify(response={
            "error": "Please input a board to be verified"
        }), 400


@app.route('/solve-board')
def solve_board():
    #TODO: solve the provided board return False if the board is unsolvable
    if request.args.get('sudo'):
        if type(request.args.get('sudo')) == str and len(request.args.get('sudo')) == 81:
            board = list_board(request.args.get('sudo'))
            if _solve(board):
                _solve(board)
                if request.args.get('stype'):
                    if request.args.get('stype').lower() == 'string':
                        return jsonify(response={
                            "board": request.args.get('sudo'),
                            "solvable": "True",
                            "solution": string_board(board)
                        }), 200
                    else:
                        return jsonify(response={
                            "board": list_board(request.args.get('sudo')),
                            "solvable": "True",
                            "solution": board
                        }), 200
                else:
                    return jsonify(response={
                        "board": list_board(request.args.get('sudo')),
                        "solvable": "True",
                        "solution": board
                    }), 200
            else:
                return jsonify(response={
                    "board": request.args.get('sudo'),
                    "solvable": "False"
                }), 200
        else:
            return jsonify(response={
                "error": "Please input a board in the right format."
            }), 400
    else:
        return jsonify(response={
            "error": "Please input a board to be solved"
        }), 400


if __name__ == "__main__":
    app.run(debug=True)
