import os
import pickle
import pandas as pd
from datetime import datetime


class Saver:

    def __init__(self, clf, method, n_groups, save_location, filename):
        self.path = save_location
        self.clf = clf
        self.method = method
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

    def save_results(self):
        folder = 'results'
        filename = self.get_result_filename()
        df = pd.DataFrame(self.clf.cv_results_)
        save_path = os.path.join(self.path, folder, filename)

        print("saving results to: " + save_path)

        df.to_csv(save_path, index=False, header=True)

    def get_result_filename(self):
        return "res_{}_{}_logocv_{}.csv".format(self.method, self.n_groups, self.filename)

    def save_params(self):
        """
        Parameter setting that gave the best results on the hold out data.
        """
        folder = 'best_params'
        filename = self.get_param_filename()
        save_path = os.path.join(self.path, folder, filename)

        print("saving best parameters to: " + save_path)

        pickle.dump(self.clf.best_params_, open(save_path, 'wb'))

    def get_param_filename(self):
        return "best_params_{}_{}.sav".format(self.method, self.filename)

    def save_best_model(self):
        """
        Estimator that was chosen by the search, i.e. estimator which gave highest score (or smallest loss if specified) on the left out data.
        """
        folder = 'models'
        filename = self.get_best_model_filename()
        save_path = os.path.join(self.path, folder, filename)

        print("saving best model to: " + save_path)

        pickle.dump(self.clf.best_estimator_, open(save_path, 'wb'))

    def get_best_model_filename(self):
        return "mod_{}_{}.sav".format(self.method, self.filename)


