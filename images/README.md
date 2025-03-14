# plots

The images contained in this folder show plots generated at different stages of
the AI players' training.

None of the data will be exactly reproducible, because of the stochastic nature of its
creation, and owing partly to the hysteresis inherent in letting an AI learn by playing
(e.g. a game might be won with a non-optimal play, which means the AI is more likely to make
the same play, with some chance it will win again, and so on)

The jubal_early player was trained from a blank state against an AI opponent (cat_blevins) that had already
been trained for 200_000 rounds, hence the early dive in its "trained" proxy value. Once it
had seen enough of the game states (which took longer than if it had been training against
another fresh opponent from the beginning), it managed to draw and win more games.

jubal_early's opponent was not reset after each game or each set of rounds, though this would
be possible if we disabled the other player's ability to update its training after
each round. It might be interesting to see what happens to the un-disabled player's game
history in that case. I suspect that more of the game states would be explored sooner, since
jubal_early wouldn't spend their whole early career being trounced by an opponent who
already has things figured out.
