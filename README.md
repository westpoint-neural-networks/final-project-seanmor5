# VeGAN

> Predicting upsets in sporting events using Generative Adversarial Networks.

VeGAN is a `tf.keras` model based on [AnoGAN](https://arxiv.org/abs/1703.05921). VeGAN is trained on over 20000 NBA matchups from 2007-2020. It assigns an *upset score* to a matchup. Higher upset scores indicate higher probabilities of upsets.

## Design

You can read a more in-depth explanation of VeGAN [here](#).

VeGAN is based off of the paper **Unsupervised Anomaly Detection with Generative Adversarial Networks**. It works by learning a distribution of Vegas Closing Lines on NBA games that resulted in the favorite winning and then predicting upsets based on the differences betweeen the learned distribution and a given sample. VeGAN reports an *upset score* which is a positive real number. Higher upset scores indicate higher probabilities of upsets.

At a high-level, the VeGAN model looks like this:

![High Level Model](assets/AnomalyDetectionModel.png?raw=true)

The generator creates odds from a provided matchup and passes them to the discriminator to determine the probability the odds are real.

The complete VeGAN model looks like this:

![Detailed VeGAN](assets/UpsetScoreModel.png?raw=true)

VeGAN was trained for 10000 Epochs using the RMSProp Optimizer. More exploration on the impact of different hyperparameters and optimizers is required.

## Usage

The easiest way to use VeGAN is with the pre-trained model. If you'd like to reproduce the results, you can use the same data used to train VeGAN located in `data/train`. For clarity, I've included the scripts used to scrape statistics from the NBA website. These scripts are pretty hacky and not nice to work with, so I recommend just using the data provided.

To detect upsets, clone this repository and then import the VeGAN model:

```python
from vegan import model.vegan.VeGAN
```

Then load the pretrained weights:

```python
vegan = VeGAN()
vegan.load_weights('vegan/model/saved_models/generator.h5', 'vegan/model/saved_models/discriminator.h5')
```

Then declare the upset detector and run on a game:

```python
upset_detector = vegan.upset_detector()
vegan.compute_upset_score(upset_detector, potential_upset, potential_upset_odds, iterations=500)
```

One of the drawbacks of this approach is that it takes a REALLY long time to run. Note that all of the trials were run with 500 iterations, so you may see different results with different numbers of iterations.

I'm working on a clean interface to get upsets using VeGAN.

## Current Results

Early Results indicate VeGAN is a viable option to detect and bet on upsets. Currently, the only betting strategy employed was betting off of various "thresholds" for upsets. For example, if VeGAN predicted an upset score of 4.2 and the upset score threshold was 4.0, a flat bet would be placed on that game. Future works will include more advanced betting strategies to maximize profitability.

Below you can see a table of the 95% Confidence Interval of profits of 10 different upset score thresholds over the course of 15 random samples seasons. A season is 5120 matchups. VeGAN ONLY makes bets on potential upsets, so it will only decide on around 2060 matchups:

![Threshold Profits](assets/ProfitThresholds.PNG?raw=true)

This table shows the 95% Confidence Interval of profits of various naive methods compared to the best upset score threshold over 15 random samples of seasons:

![Different Method Profits](/assets/ProfitMethods.png?raw=true)

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

If you find any issues with VeGAN you can open an issue or submit a pull request. You can also get in contact with me directly [here](mailto:smoriarity.5@gmail.com).

## References and Credit

Code implementations were tweaked from the examples from:

* [Keras AnoGAN](https://github.com/tkwoo/anogan-keras)
* [Keras GAN](https://github.com/eriklindernoren/Keras-GAN)

Research References (used in paper):

[1]	I. Goodfellow et al., “Generative Adversarial Nets,” in Advances in Neural Information Processing Systems 27, Z. Ghahramani, M. Welling, C. Cortes, N. D. Lawrence, and K. Q. Weinberger, Eds. Curran Associates, Inc., 2014, pp. 2672–2680.
[2]	A. Radford, L. Metz, and S. Chintala, “UNSUPERVISED REPRESENTATION LEARNING WITH DEEP CONVOLUTIONAL GENERATIVE ADVERSARIAL NETWORKS,” p. 16, 2016.
[3]	T. Schlegl, P. Seeböck, S. M. Waldstein, U. Schmidt-Erfurth, and G. Langs, “Unsupervised Anomaly Detection with Generative Adversarial Networks to Guide Marker Discovery,” arXiv:1703.05921 [cs], Mar. 2017, Accessed: Apr. 09, 2020. [Online]. Available: http://arxiv.org/abs/1703.05921.
[4]	P. Z. Maymin, “Wage against the machine: A generalized deep-learning market test of dataset value,” International Journal of Forecasting, vol. 35, no. 2, pp. 776–782, Apr. 2019, doi: 10.1016/j.ijforecast.2017.09.008.
[5]	O. Hubáček, G. Šourek, and F. Železný, “Exploiting sports-betting market using machine learning,” International Journal of Forecasting, vol. 35, no. 2, pp. 783–796, Apr. 2019, doi: 10.1016/j.ijforecast.2019.01.001.
[6]	F. Di Mattia, P. Galeone, M. De Simoni, and E. Ghelfi, “A Survey on GANs for Anomaly Detection,” arXiv:1906.11632 [cs, stat], Jun. 2019, Accessed: Apr. 09, 2020. [Online]. Available: http://arxiv.org/abs/1906.11632.
[7]	A. L. Maas, A. Y. Hannun, and A. Y. Ng, “Rectiﬁer Nonlinearities Improve Neural Network Acoustic Models,” p. 6.
[8]	S. Ioffe and C. Szegedy, “Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift,” arXiv:1502.03167 [cs], Mar. 2015, Accessed: Apr. 30, 2020. [Online]. Available: http://arxiv.org/abs/1502.03167.

