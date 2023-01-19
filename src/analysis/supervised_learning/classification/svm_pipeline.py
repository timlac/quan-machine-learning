import os

import numpy as np
import pandas as pd
import json

from sklearn.model_selection import GridSearchCV

from sklearn.svm import SVC
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

import seaborn as sns

from global_config import ROOT_DIR, AU_INTENSITY_COLS, GAZE_COLS, POSE_COLS, \
    AUDIO_FUNCTIONALS_EGEMAPS_COLS, emotion_abr_to_emotion
from src.analysis.supervised_learning.evaluation.confusion_matrix import ConfusionMatrixCreator, conf_mat_to_df, \
    plot_conf_matrix


from src.preprocessing.dataset_creation.scaling.functional_scaling import functional_scale_by
from src.preprocessing.dataset_creation.scaling.low_level_scaling import low_level_scale_by


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
                  'C': [1, 10],
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


def check_alignment(sli, df):
    y_sli = get_fixed_col(sli, "emotion_1_id")
    y_df = df["emotion_1_id"].values
    print(np.array_equal(y_sli, y_df))

    y_sli = get_fixed_col(sli, "video_id")
    y_df = df["video_id"].values
    print(np.array_equal(y_sli, y_df))


path_video = os.path.join(ROOT_DIR, "files/out/openface_query_FULL.csv")
df_video = pd.read_csv(path_video)

path_audio = os.path.join(ROOT_DIR, "files/out/opensmile_functionals_query_FULL.csv")
df_audio = pd.read_csv(path_audio)

slices_video = slice_by(df_video, "filename")
interpolator = Interpolator([*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS])
slices_video = interpolator.remove_interpolate(slices_video)

slices_video, df_audio = align_audio_video(slices_video, df_audio)

check_alignment(slices_video, df_audio)

y_audio_video = get_fixed_col(slices_video, "emotion_1_id")
video_ids = get_fixed_col(slices_video, "video_id")


def transform_video_modality(sli, cols):
    x = get_cols(sli, cols)
    x = low_level_scale_by(slices=x,
                           by=video_ids,
                           method="standard")

    x_agg = get_aggregate_measures(x)
    scaler = MinMaxScaler()
    return scaler.fit_transform(x_agg)


class Evaluator:
    conf_mat_save_path = os.path.join(ROOT_DIR,
                                      "files/out/functionals/supervised_learning/confusion_matrix_")
    classification_report_save_path = os.path.join(ROOT_DIR,
                                      "files/out/functionals/supervised_learning/classification_report_")

    def __init__(self, x, y, model_parameters, save_as):
        self.x = x
        self.y = y
        self.clf = SVC(**model_parameters, probability=True)
        self.save_as = save_as

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
        df_cm.to_csv(self.conf_mat_save_path + self.save_as + ".csv", index=False)
        plot_conf_matrix(df_cm, title="Normalized Confusion Matrix", save_path=self.conf_mat_save_path + self.save_as)

    def create_classification_report(self):
        splits = self.get_splits()
        y_pred = cross_val_predict(self.clf, self.x, self.y, cv=splits, n_jobs=-1)
        report = metrics.classification_report(y_true=self.y, y_pred=y_pred,
                                               target_names=emotion_abr_to_emotion.values(),
                                               output_dict=True)

        with open(self.classification_report_save_path + self.save_as + ".json", 'w') as fp:
            json.dump(report, fp)


def print_scores(scores, scoring_method):
    print('printing {} measures'.format(scoring_method))
    print('avg (train):', np.mean(scores['train_{}'.format(scoring_method)]))
    print('std (train):', np.std(scores['train_{}'.format(scoring_method)]))
    print('avg (validation):', np.mean(scores['test_{}'.format(scoring_method)]))
    print('std (validation):', np.std(scores['test_{}'.format(scoring_method)]))


# for col in [("action_units", AU_INTENSITY_COLS), ("gaze", GAZE_COLS), ("pose", POSE_COLS)]:
#     print(col[0])
    # x = transform_video_modality(slices_video, col[1])
    # clf = param_search(x, y_audio_video)
    # eval = Evaluator(x, y_audio_video, clf.best_params_, col[0])
    # eval.evaluate_scores("accuracy")
    # eval.evaluate_scores("roc_auc_ovo_weighted")
    # eval.evaluate_confusion_matrix()
    # eval.create_classification_report()


# au_gaze_pose = transform_video_modality(slices_video, [*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS])
#
# egemaps = df_audio[AUDIO_FUNCTIONALS_EGEMAPS_COLS].values
# egemaps = functional_scale_by(egemaps, video_ids, "min_max")
# clf = param_search(egemaps, y_audio_video)
#
# eval = Evaluator(egemaps, y_audio_video, clf.best_params_, "audio")
# eval.evaluate_scores("accuracy")
# eval.evaluate_scores("roc_auc_ovo_weighted")


#
# all_modes = np.hstack((au_gaze_pose, egemaps))
#
#
# clf = param_search(all_modes, y_audio_video)
#
# eval = Evaluator(all_modes, y_audio_video, clf.best_params_, "all_modes")
# eval.evaluate_scores("accuracy")
# eval.evaluate_scores("roc_auc_ovo_weighted")
# eval.evaluate_confusion_matrix()
# eval.create_classification_report()


