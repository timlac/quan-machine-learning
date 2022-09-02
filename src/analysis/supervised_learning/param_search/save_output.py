import os
import pickle
import pandas as pd
from datetime import datetime


class Saver:

    def __init__(self, clf, method, group_type, n_groups, save_location, filename):
        self.path = save_location
        self.clf = clf
        self.method = method
        self.group_type = group_type
        self.n_groups = n_groups
        self.filename = filename

    def save(self):
        print("successfully trained {} classifier".format(self.method))
        print("best estimator:")
        print(self.clf.best_estimator_)
        print()
        print("best params:")
        print(self.clf.best_params_)
        print("saving at time {}".format(datetime.now()))

        self.save_results()
        self.save_params()
        self.save_best_model()

    def get_save_string(self):
        return "{}_{}_{}_logocv_{}".format(self.method, self.group_type, self.n_groups, self.filename)

    def save_results(self):
        df = pd.DataFrame(self.clf.cv_results_)

        folder = 'results'
        filename = "{}_{}.csv".format("results", self.get_save_string())
        save_path = os.path.join(self.path, folder, filename)

        print("saving results to: " + save_path)
        df.to_csv(save_path, index=False, header=True)

    def save_params(self):
        """
        Parameter setting that gave the best results on the hold out data.
        """
        folder = 'best_params'
        filename = "{}_{}.sav".format("best_params", self.get_save_string())
        save_path = os.path.join(self.path, folder, filename)

        print("saving best parameters to: " + save_path)
        pickle.dump(self.clf.best_params_, open(save_path, 'wb'))

    def save_best_model(self):
        """
        Estimator that was chosen by the search, i.e. estimator which gave highest score
        (or smallest loss if specified) on the left out data.
        """
        folder = 'models'
        filename = "{}_{}.sav".format("model", self.get_save_string())
        save_path = os.path.join(self.path, folder, filename)

        print("saving best model to: " + save_path)
        pickle.dump(self.clf.best_estimator_, open(save_path, 'wb'))


def main():
    s = Saver(clf=None, method="svm", group_type="twinned", n_groups="5", save_location=None, filename="au_video")
    print(s.get_save_string())


if __name__ == "__main__":
    main()