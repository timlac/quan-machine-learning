import pandas as pd


def refactor_duplicate_columns(df):
    """
    openface generates case sensitive, duplicate columns, rename these with
    2d and 3d specifications
    """
    df.columns = df.columns.str.replace('eye_lmk_y', 'eye_2d_lmk_y')
    df.columns = df.columns.str.replace('eye_lmk_x', 'eye_2d_lmk_x')
    df.columns = df.columns.str.replace('eye_lmk_Y', 'eye_3d_lmk_y')
    df.columns = df.columns.str.replace('eye_lmk_X', 'eye_3d_lmk_x')

    df.columns = df.columns.str.replace('^x_', 'x_2d_', regex=True)
    df.columns = df.columns.str.replace('^y_', 'y_2d_', regex=True)
    df.columns = df.columns.str.replace('^X_', 'x_3d_', regex=True)
    df.columns = df.columns.str.replace('^Y_', 'y_3d_', regex=True)

    df.columns = df.columns.str.replace('^z_', 'z_2d_', regex=True)
    df.columns = df.columns.str.replace('^Z_', 'z_3d_', regex=True)
    return df
