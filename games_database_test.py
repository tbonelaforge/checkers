from games_database import record_game, read_all_games

if __name__ == "__main__":
    # print("Successfully imported the record_game function: ")
    # print(record_game)
    # print("About to record the following 'game'")
    # fake_game = [{'foo': "bar"}]
    # record_game(fake_game)
    # print("Done! now check the database! (filesystem...)")

    print("Reading all games from the database...")
    for move_history in read_all_games():
        print("Yielded move_history: ")
        print(move_history)