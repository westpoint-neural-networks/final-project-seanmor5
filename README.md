# VeGAN

> Predicting upsets in sporting events using Generative Adversarial Networks.

VeGAN is a `tf.keras` model based on [AnoGAN](https://arxiv.org/abs/1703.05921). VeGAN is trained on over 20000 NBA matchups from 2007-2020. It assigns an *upset score* to a matchup. Higher upset scores indicate higher probabilities of upsets.

## Design

You can read a more in-depth explanation of VeGAN [here](#).

VeGAN is based off of the paper **Unsupervised Anomaly Detection with Generative Adversarial Networks**. It works by learning a distribution of Vegas Closing Lines on NBA games that resulted in the favorite winning and then predicting upsets based on the differences betweeen the learned distribution and a given sample. VeGAN reports an *upset score* which is a positive real number. Higher upset scores indicate higher probabilities of upsets.

At a high-level, the VeGAN model looks like this:

![High Level Model](https://www.github.com/seanmor5/final-project/assets/AnomalyDetectionModel.png)

The generator creates odds from a provided matchup and passes them to the discriminator to determine the probability the odds are real.

The complete VeGAN model looks like this:

![Detailed VeGAN](https://www.github.com/seanmor5/final-project/assets/UpsetScoreModel.png)

VeGAN was trained for 10000 Epochs using the RMSProp Optimizer. More exploration on the impact of different hyperparameters and optimizers is required.

## Usage

## Current Results

Early Results indicate VeGAN is a viable option to detect and bet on upsets. Currently, the only betting strategy employed was betting off of various "thresholds" for upsets. For example, if VeGAN predicted an upset score of 4.2 and the upset score threshold was 4.0, a flat bet would be placed on that game. Future works will include more advanced betting strategies to maximize profitability.

Below you can see a table of the 95% Confidence Interval of profits of 10 different upset score thresholds over the course of 15 random samples seasons. A season is 5120 matchups. VeGAN ONLY makes bets on potential upsets, so it will only decide on around 2060 matchups:

![Threshold Profits](https://www.github.com/seanmor5/final-project/assets/ProfitThresholds.PNG)

This table shows the 95% Confidence Interval of profits of various naive methods compared to the best upset score threshold over 15 random samples of seasons:

![Different Method Profits](https://www.github.com/seanmor5/final-project/assets/ProfitMethods.png)

The most important result here is that VeGAN significantly outperforms the Random Upset Baseline. Random Upsets filters a season to only include potential upsets and then randomly decides to bet on around 50% of the matchups. The results show that VeGAN performs better than just random guessing---indicating it learns some criteria to select upsets.

## Future Works

VeGAN makes bets on basic box score statistics. It has no way of accounting for: injuries, trades, hot streaks, team performance in different stadiums, individual player matchups, etc.

In the future, the following approaches will be applied to VeGAN in hopes of building on the results achieved with basic box score statistics:

* Using CNN with indivdual player statistics
* Using CNN with a teams quarter-by-quarter statistics
* Using CNN with windows of games
* Using RNN with windows of games

Additionally, exploration of different betting strategies is required. Such as:

* Integration with Reinforcement Learning to learn best Betting Strategy
* Translation of upset scores to probabilities for Kelly Criterion
* Integration of Portfolio Optimization for better bets
* Integration of Imitation Learning to tail handicappers

Finally, I hope to expand VeGAN to other sports and other types of bets. I also plan to create a friendly web interface for serving VeGAN's predictions.

## Contributing

## References and Credit


