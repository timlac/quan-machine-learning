import os
import sys
import pickle

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix

import seaborn as sns

from global_config import ROOT_DIR, emotion_id_to_emotion_abr, conf_cmap, AU_INTENSITY_COLS, GAZE_COLS, POSE_COLS, \
    AUDIO_FUNCTIONALS_EGEMAPS_COLS, emotion_abr_to_emotion
from src.analysis.supervised_learning.evaluation.confusion_matrix import ConfusionMatrixCreator, conf_mat_to_df, \
    plot_conf_matrix

from src.analysis.data_exploration import plot_time_series_means_subplots

from src.preprocessing.dataset_creation.scaling.functional_scaling import functional_scale_by
from src.preprocessing.dataset_creation.scaling.low_level_scaling import low_level_scale_by

from src.utils.helpers import mapper

from src.preprocessing.dataset_creation.helpers import slice_by, get_cols, get_fixed_col
from src.preprocessing.dataset_creation.aggregation import get_aggregate_measures
from src.preprocessing.dataset_creation.interpolation import Interpolator
from src.preprocessing.dataset_creation.fusion import align_audio_video


def param_search(x, y):
    # regularization parameter, lower C -> more regularization,
    # large C -> less regularization
    c_values = [0.1, 1, 5, 10, 25, 50, 75, 100]

    gamma = [1, 0.1, 0.01, 0.001, 0.0001]

    kernel = ['rbf', 'linear', 'poly', 'sigmoid']

    parameters = {'class_weight': ['balanced'],
                  'C': c_values,
                  'gamma': gamma,
                  'kernel': kernel,
                  }

    parameters = {'class_weight': ['balanced'],
                  'C': [1],
                  'gamma': [1],
                  'kernel': ["linear"],
                  }

    skf = StratifiedKFold(n_splits=5, shuffle=True)

    svc = SVC()
    clf = GridSearchCV(estimator=svc,
                       param_grid=parameters,
                       scoring='accuracy',
                       verbose=5,
                       cv=skf.split(x, y),
                       n_jobs=-1,
                       )

    clf.fit(x, y)
    print(clf.best_params_)
    return clf


def evaluate_scores(x, y, svc, splits, scoring_method):
    scores = cross_validate(X=x, y=y,
                            estimator=svc,
                            scoring=[scoring_method],
                            verbose=1,
                            cv=splits,
                            n_jobs=-1,
                            return_train_score=True
                            )

    print('printing {} measures'.format(scoring_method))
    print('avg (train):', np.mean(scores['train_{}'.format(scoring_method)]))
    print('std (train):', np.std(scores['train_{}'.format(scoring_method)]))
    print('avg (validation):', np.mean(scores['test_{}'.format(scoring_method)]))
    print('std (validation):', np.std(scores['test_{}'.format(scoring_method)]))


def check_alignment(sli, df):
    y_sli = get_fixed_col(sli, "emotion_1_id")
    y_df = df["emotion_1_id"].values
    print(np.array_equal(y_sli, y_df))

    y_sli = get_fixed_col(sli, "video_id")
    y_df = df["video_id"].values
    print(np.array_equal(y_sli, y_df))


path_video = os.path.join(ROOT_DIR, "files/out/openface_query.csv")
df_video = pd.read_csv(path_video)

path_audio = os.path.join(ROOT_DIR, "files/out/opensmile_functionals_query.csv")
df_audio = pd.read_csv(path_audio)

video_cols = [*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS]
slices = slice_by(df_video, "filename")
interpolator = Interpolator(video_cols)
slices = interpolator.remove_interpolate(slices)

slices, df_audio = align_audio_video(slices, df_audio)

check_alignment(slices, df_audio)

y_audio_video = get_fixed_col(slices, "emotion_1_id")
video_ids = get_fixed_col(slices, "video_id")


def transform_video_modality(sli, cols):
    x = get_cols(sli, cols)
    x = low_level_scale_by(slices=x,
                           by=video_ids,
                           method="standard")

    x_agg = get_aggregate_measures(x)
    scaler = MinMaxScaler()
    return scaler.fit_transform(x_agg)


def run_modality(x, y):
    clf = param_search(x, y)
    svc = SVC(**clf.best_params_)
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    splits = skf.split(x, y)
    evaluate_scores(x, y, svc, splits, scoring_method="accuracy")
    return clf, splits


class Evaluator:
    conf_mat_save_path = os.path.join(ROOT_DIR,
                                      "files/out/functionals/supervised_learning/confusion_matrix_all_modes")

    def __init__(self, x, y, model_parameters):
        self.x = x
        self.y = y
        self.clf = SVC(**model_parameters, probability=True)

    def get_splits(self):
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=10)
        return skf.split(self.x, self.y)

    def evaluate_scores(self, scoring_method):
        splits = self.get_splits()
        scores = cross_validate(X=self.x, y=self.y,
                                estimator=self.clf,
                                scoring=[scoring_method],
                                verbose=1,
                                cv=splits,
                                n_jobs=-1,
                                return_train_score=True
                                )
        print_scores(scores, scoring_method)

    def evaluate_confusion_matrix(self):
        splits = self.get_splits()
        conf_mat_creator = ConfusionMatrixCreator(self.clf)
        cm = conf_mat_creator.calculate_avg_conf_matrix(self.x, self.y, splits)
        df_cm = conf_mat_to_df(cm, self.y)
        df_cm.to_csv(self.conf_mat_save_path + ".csv", index=False)
        plot_conf_matrix(df_cm, title="Normalized Confusion Matrix", save_path=self.conf_mat_save_path)

    def create_classification_report(self):
        splits = self.get_splits()
        y_pred = cross_val_predict(self.clf, self.x, self.y, cv=splits)
        report = metrics.classification_report(y_true=self.y, y_pred=y_pred,
                                               target_names=emotion_abr_to_emotion.values())
        print(report)

        matrix = confusion_matrix(self.y, y_pred)
        df = pd.DataFrame(matrix)
        df.to_csv(self.conf_mat_save_path + "_custom.csv")


def print_scores(scores, scoring_method):
    print('printing {} measures'.format(scoring_method))
    print('avg (train):', np.mean(scores['train_{}'.format(scoring_method)]))
    print('std (train):', np.std(scores['train_{}'.format(scoring_method)]))
    print('avg (validation):', np.mean(scores['test_{}'.format(scoring_method)]))
    print('std (validation):', np.std(scores['test_{}'.format(scoring_method)]))


# au = transform_video_modality(slices, AU_INTENSITY_COLS)
# run_modality(au, y_audio_video)
#
# gaze = transform_video_modality(slices, GAZE_COLS)
# run_modality(gaze, y_audio_video)
#
# pose = transform_video_modality(slices, POSE_COLS)
# run_modality(pose, y_audio_video)
#
au_gaze_pose = transform_video_modality(slices, [*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS])
# run_modality(au_gaze_pose, y_audio_video)
#
egemaps = df_audio[AUDIO_FUNCTIONALS_EGEMAPS_COLS].values
egemaps = functional_scale_by(egemaps, video_ids, "min_max")
# run_modality(egemaps, y_audio_video)

all_modes = np.hstack((au_gaze_pose, egemaps))


clf = param_search(all_modes, y_audio_video)

eval = Evaluator(all_modes, y_audio_video, clf.best_params_)
eval.evaluate_scores("accuracy")
eval.evaluate_scores("roc_auc_ovo_weighted")
eval.evaluate_confusion_matrix()
eval.create_classification_report()
