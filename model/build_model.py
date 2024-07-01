import pickle

from sklearn import datasets
from sklearn.ensemble import GradientBoostingClassifier


def build_model():
    """
    Build naive IRIS model.
    
    Iris contains 150 rows and 4 features per row.
    Sepal Length, Sepal Width, Petal Length and Petal Width.
    """
    iris = datasets.load_iris()
    X = iris.data
    Y = iris.target

    clf = GradientBoostingClassifier()
    clf.fit(X, Y)

    pickle.dump(clf, open('./resources/model.pkl', 'wb'))

if __name__ == "__main__":
    build_model()