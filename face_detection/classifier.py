# from features import *
from .features import *


WINDOW_SIZE = 18


def to_integral(img):
    integral = np.cumsum(np.cumsum(img, axis=0), axis=1)
    return np.pad(integral, (1, 1), 'constant', constant_values=(0, 0))[:-1, :-1]


def gamma(values, coeff=2.2):
    return values**(1./coeff)


class weakClassifier:
    def __init__(self, feature, threshold, polarity, alpha=None):
        self.feature = feature
        self.threshold = threshold
        self.polarity = polarity
        self.alpha = alpha

    def run(self, i):
        if((self.polarity * self.feature(i)) < (self.polarity * self.threshold)):
            return 1.0
        else:
            return 0.0


class Classifier:
    def __init__(self, weakClassifiersList):
        self.weakClassifiers = weakClassifiersList

    def isFace(self, ii, sum_hy=0., sum_al=0.):
        sum_hypotheses = sum_hy
        sum_alphas = sum_al
        for c in self.weakClassifiers:
            sum_hypotheses += c.alpha * c.run(ii)
            sum_alphas += c.alpha
        prop = (sum_hypotheses) / (.5*sum_alphas)
        return prop, sum_hypotheses, sum_alphas
