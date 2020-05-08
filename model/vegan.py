from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LeakyReLU, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.backend as K
import os

class VeGAN():

  def __init__(self, optimizer):

    # Build generator `G`
    self.G = self.build_generator()
    
    # Build discriminator `D`
    self.D = self.build_discriminator()
    self.D.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    
    # Both `D` and `G` accept a vector of 174 team statistics
    inp = Input(shape=(174,))

    # Generate `odds` from `G`
    odds = self.G(inp)

    # Are `odds` valid given `inp`?
    valid = self.D(inputs=[inp, odds])

    # Combined model for overall generator training
    self.combined = Model(inp, valid)
    self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

  def build_generator(self):
    # Input is a vector of 174 team statistics
    inp = Input(shape=(174,))
    
    # First Block
    fc1 = Dense(128)(inp)
    fc1 = LeakyReLU(alpha=0.2)(fc1)
    fc1 = BatchNormalization(momentum=0.8)(fc1)

    # Second Block
    fc2 = Dense(64)(fc1)
    fc2 = LeakyReLU(alpha=0.2)(fc2)

    # Final Prediction, inverse of decimal odds
    odds = Dense(1, activation='sigmoid')(fc2)

    return Model(inp, odds)
  
  def build_discriminator(self):
    # Discriminator takes two inputs, stats and odds
    inp = Input(shape=(174,))
    odds = Input(shape=(1,))

    # First Block
    fc1 = Dense(128)(inp)
    fc1 = LeakyReLU(alpha=0.2)(fc1)
    fc1 = Dropout(0.2)(fc1)

    # Second Block
    fc2 = Dense(64)(fc1)
    fc2 = LeakyReLU(alpha=0.2)(fc2)
    fc2 = Dropout(0.2)(fc2)

    # Concat transformed stats with odds
    combined = K.concatenate([fc2, odds])
    
    # Make prediction, probability odds are real
    pred = Dense(1, activation='sigmoid')(combined)

    return Model(inputs=[inp, odds], outputs=pred)
  
  def save_weights(self, path):
    d_path = os.path.join(path, 'discriminator.h5')
    g_path = os.path.join(path, 'generator.h5')
    self.G.save_weights(g_path)
    self.D.save_weights(d_path)

  def load_weights(self, d_path, g_path):
    self.G.load_weights(g_path)
    self.D.load_weights(d_path)

  # See Keras AnoGAN: https://github.com/tkwoo/anogan-keras/blob/master/anogan.py
  def feature_extractor(self):
    # Feature extractor determines difference between features of true, generated odds
    intermediate = Model(inputs=self.D.layers[0].input, outputs=self.D.layers[-7].output)
    intermediate.compile(loss='binary_crossentropy', optimizer='rmsprop')
    return intermediate

  # See Keras AnoGAN: https://github.com/tkwoo/anogan-keras/blob/master/anogan.py
  def sum_of_residual(self, y_true, y_pred):
    return K.sum(K.abs(y_true - y_pred))

  # See Keras AnoGAN: https://github.com/tkwoo/anogan-keras/blob/master/anogan.py
  def upset_detector(self):
    fe = self.feature_extractor()
    fe.trainable = False
    g = Model(inputs=self.G.layers[1].input, outputs=self.G.layers[-1].output)
    g.trainable = False

    aInp = Input(shape=(174,))
    gInp = Dense((174), activation='sigmoid', trainable=True)(aInp)

    # Generate odds
    gOut = g(gInp)
    # Get some features from generated odds
    dOut = fe([aInp, gOut])
    # Determine difference of features, true odds from sum of residual
    model = Model(inputs=aInp, outputs=[gOut, dOut])
    model.compile(loss=self.sum_of_residual, loss_weights=[0.9, 0.1], optimizer='rmsprop')
    # This is a TEST ONLY model
    K.set_learning_phase(0)

    return model

  # See Keras AnoGAN: https://github.com/tkwoo/anogan-keras/blob/master/anogan.py
  def compute_upset_score(self, model, x, y, iterations=500):
      intermediate = self.feature_extractor()
      d_x = intermediate.predict([x, y])

      # Have to fit over several iterations to accumulate loss (upset score)
      loss = model.fit(x, [y, d_x], batch_size=1, epochs=iterations, verbose=0)

      # Similar data is irrelvant in this case, kept for consistency
      similar_data, _ = model.predict(x)
      
      loss = loss.history['loss'][-1]
      
      return loss, similar_data

  # Helper for running on a season of upsets
  def compute_upset_scores(self, model, x, y, iterations=500):
    upset_scores = []

    for line, odd in zip(X_underdogs, underdog_odds):
      score, _ = vegas.compute_upset_score(model, np.array([line]), np.array([odd]))
      upset_scores.append(score)

    return np.array(upset_scores)

  # Tweaked from Keras GAN implementations: https://github.com/eriklindernoren/Keras-GAN
  def train(self, X_train, y_train, results=None, epochs=10, batch_size=128):
  
    valid = np.ones((batch_size, 1))
    fake = np.zeros((batch_size, 1))

    for epoch in range(epochs):
      
      idx = np.random.randint(0, X_train.shape[0], batch_size)

      games = X_train[idx]
      outcomes = results[idx]
  
      gen_odds = self.G.predict(games)
      odds = y_train[idx]
      accept = self.D.predict([games, gen_odds])

      d_loss_real = self.D.train_on_batch([games, odds], valid)
      d_loss_fake = self.D.train_on_batch([games, gen_odds], fake)
      d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

      g_loss = self.combined.train_on_batch(games, valid)

      print ("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss))