from django.test import TestCase
from game_api.models import Game

from django.core.exceptions import ValidationError

class GameModelTests( TestCase ):

    ### word field
    def test_init_should_assign_given_word(self):
        game = Game( word= "TESTWORD")
        self.assertEqual( game.word, "TESTWORD" )

    def test_word_is_required( self ):
        with self.assertRaises( ValidationError ):
            game = Game()
            game.full_clean()

    def test_word_is_less_than_3_chars( self ):
        with self.assertRaises( ValidationError ):
            game = Game( word = "AA")
            game.full_clean()

    def test_word_is_only_letters( self ):
        with self.assertRaises( ValidationError ):
            game = Game( word = "A1B")
            game.full_clean()



    ### guesses_taken field
    def test_guesses_taken_should_not_increment_if_letter_in_word( self ):
        expectedGuessesTaken = 2
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5,
            guesses_taken= expectedGuessesTaken
        )

        game.handleGuess('T')
        self.assertEqual( expectedGuessesTaken, game.guesses_taken )

    def test_guesses_taken_should_increment_if_letter_not_in_word( self ):
        expectedGuessesTaken = 2
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5,
            guesses_taken= expectedGuessesTaken
        )

        game.handleGuess('X')
        self.assertEqual( expectedGuessesTaken +1, game.guesses_taken )


    ### guessed_word_state field
    def test_guessed_word_state_is_unchanged_if_guess_not_in_word( self ):
        initialGuessedWordState = ['','','S','','W','O','R','']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= initialGuessedWordState,
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5,
            guesses_taken= 2
        )

        game.handleGuess('X')
        self.assertEqual( initialGuessedWordState, game.guessed_word_state )

    def test_guessed_word_state_is_updated_with_guessed_letter_in_word( self ):
        initialGuessedWordState = ['','','S','','W','O','R','']
        expectedGuessedWordState = ['T','','S','T','W','O','R','']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= initialGuessedWordState,
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5,
            guesses_taken= 2
        )

        game.handleGuess('T')
        self.assertEqual( expectedGuessedWordState, game.guessed_word_state )


    ### available_letters field
    def test_init_should_set_letters_available_to_alphabet( self ):
        game = Game( word= "TESTWORD")
        self.assertEqual( game.letters_available, list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    def test_available_letters_should_remove_guessed_letters_when_letter_in_word( self ):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            letters_available = initialLettersAvailable,
            guesses_allowed= 5,
            guesses_taken= 2
        )

        guess = 'T'

        game.handleGuess(guess)
        expectedLettersAvailable = [letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEqual( game.letters_available, expectedLettersAvailable )

    def test_available_letters_should_remove_guessed_letters_when_letter_not_in_word( self ):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            letters_available = initialLettersAvailable,
            guesses_allowed= 5,
            guesses_taken= 2
        )

        guess = 'Q'

        game.handleGuess(guess)
        expectedLettersAvailable = [letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEqual( game.letters_available, expectedLettersAvailable )

    ### letters_guessed field
    def test_letters_guessed_should_add_guessed_letter_when_letter_in_word( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 5,
            guesses_taken= 2
        )

        guess = 'T'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEqual( game.letters_guessed, expectedLettersGuessed )

    def test_letters_guessed_should_add_guessed_letter_when_letter_not_in_word( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 5,
            guesses_taken= 2
        )

        guess = 'Q'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEqual( game.letters_guessed, expectedLettersGuessed )

    ### is_game_over field
    # TODO: add tests
    # HINT: considering adding a fixture or other widely scoped variables if you feel that will
    #  make this easier

    def test_is_game_over_is_false_if_guesses_left( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 10,
            guesses_taken= 6
            )

        guess = 'Q'
        game.handleGuess(guess)
        self.assertTrue(game.guesses_taken < game.guesses_allowed)
        # self.assertEqual(game.is_game_over, False)
        self.assertFalse(game.is_game_over)

    def test_is_game_over_is_false_if_not_all_letters_guessed( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 10,
            guesses_taken= 6
            )

        guess = 'Q'
        game.handleGuess(guess)
        self.assertTrue('' in game.guessed_word_state)
        # self.assertEqual(game.is_game_over, False)
        self.assertFalse(game.is_game_over)

    def test_is_game_over_is_true_if_no_guesses_left( self ):
        initialLettersGuessed = ['T','E','S', 'A', 'W', 'O', 'R','C','U']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['T','E','S','T','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 10,
            guesses_taken= 9
            )

        guess = 'Q'
        game.handleGuess(guess)
        self.assertTrue(game.guesses_taken == game.guesses_allowed)
        # self.assertEqual(game.is_game_over, True)
        self.assertTrue(game.is_game_over)

    def test_is_game_over_is_true_if_all_letters_guessed( self ):
        initialLettersGuessed = ['T','E','S', 'A', 'W', 'O', 'R','C','U']
        game = Game(
            word= 'TESTWORD',
            guessed_word_state= ['T','E','S','T','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 10,
            guesses_taken= 9
            )

        guess = 'D'
        game.handleGuess(guess)
        self.assertTrue('' not in game.guessed_word_state)
        # self.assertEqual(game.is_game_over, True)
        self.assertTrue(game.is_game_over)
