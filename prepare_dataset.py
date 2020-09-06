import os
import uuid
import shutil
import chess.pgn
import io


def prep_dataset(dataset_dir, dataset_file, rr='ALL'):
    pgn_dir = os.path.join(dataset_dir, 'kaggle_pgn_' + str(rr))
    try:
        shutil.rmtree(pgn_dir)
    except FileNotFoundError:
        pass
    try:
        os.mkdir(pgn_dir)
    except FileExistsError:
        pass
    with open(dataset_file, 'r') as f:
        if rr == 'ALL':
            chunk = f.read()
        else:
            chunk = f.read(rr)
        lines = chunk.split('\n')[5:]
        for game in lines:
            sbuf = game.split("###")
            result = sbuf[0].split(' ')[2]
            game_obj = chess.pgn.read_game(io.StringIO(sbuf[1]))
            if game_obj:
                game_obj.headers['Result'] = result
                try:
                    print(game_obj, file=open(os.path.join(
                        pgn_dir, str(uuid.uuid4())+'.pgn'), 'w'), end='\n\n')
                except ValueError:
                    pass


if __name__ == "__main__":
    from dataset import dataset_dir, dataset_file
    prep_dataset(dataset_dir, dataset_file, rr='ALL')
