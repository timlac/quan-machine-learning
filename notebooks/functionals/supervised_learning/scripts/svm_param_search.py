import argparse
import os
import numpy as np 
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import pickle

def parse_args():
    """
    Parse arguments.
    """
    parser = argparse.ArgumentParser()
    
    # data directories
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    # parser.add_argument("--test", type=str, default=os.environ.get("SM_CHANNEL_TEST"))

    # model directory: we will use the default set by SageMaker, /opt/ml/model
    parser.add_argument("--model_dir", type=str, default=os.environ.get("SM_MODEL_DIR"))

    return parser.parse_known_args()

def get_train_data(path):
    
    print(os.listdir(path))
    
    files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith("npz")]
    
    if len(files) == 0:
        raise ValueError("Invalid # of files in dir: {}".format(path))
    
    f = np.load(files[0])

    x = f['x']
    y = f['y']
    
    print('x:', x.shape,'y:', y.shape)

    return x, y


def start(args):
    
    print("printing args")
    print(args)
    
    print("printing args.train: ")
    print(args.train)
    print("done printing args train")
    x, y = get_train_data(args.train)
    svm = SVM()
    clf = svm.param_search(x, y)
    pickle.dump(clf, open(os.path.join(args.model_dir, "model.pickle"), 'wb'))


class SVM:
    # Define parameters to evaluate
    # defining parameter range
    c_values = [0.1, 1, 10, 100, 1000]
    gamma = [1, 0.1, 0.01, 0.001, 0.0001]
    kernel = ['rbf', 'linear', 'poly', 'sigmoid']

    parameters = {'class_weight': ['balanced'],
                  'C': c_values,
                  'gamma': gamma,
                  'kernel': kernel,
                  }

    @classmethod
    def param_search(cls, x, y):

        svc = SVC()

        clf = GridSearchCV(estimator=svc,
                           param_grid=cls.parameters,
                           scoring='accuracy',
                           verbose=51,
                           n_jobs=-1,
                           )

        clf.fit(x, y)
        return clf
    

if __name__ == "__main__":
    
    args, _ = parse_args()

    start(args)