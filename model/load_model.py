import pickle


def load_model():
    """
    Load a previously built model from disk.x

    This module is not used anywhere in the deployment.
    Provided only to demonstrate the trained model is used.
    """

    # 0,1,2 (Setosa, Versicolour, and Virginica)
    output_classes = {
        0: "Setosa",
        1: "Versicolour",
        2: "Virginica"
    }

    model = pickle.load(open('./resources/model.pkl', mode='r+b'))
    prediction = model.predict([[7.2, 3.6, 4.1, 5.0]])
    print(prediction) # Prints the predicted label.
    print(model.classes_) # Prints the possible output classes.
    print(output_classes[prediction[0]])

if __name__ =="__main__":
    load_model()