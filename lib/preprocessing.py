import pandas as pd
import regex as re

def prepare_data(path: str) -> pd.DataFrame:
    """ Load and prepare/preprocess the data

    Parameters:
    -----------

    path : str
        Path to the dataset, file should be in csv.

    Returns:
    --------

    df : pandas.core.frame.DataFrame
        The preprocessed data to be used for the analyses of thesis subjects.
    """

    df = pd.read_csv(path)
    df.Date = pd.to_datetime(df.Date)
    df.Time = pd.to_datetime(df.Time)
    df['Grade'] = df['Grade'].apply(fix_faculty_typing)
    return df


def fix_faculty_typing(string: str) -> str:
    return re.sub('Faculte','Faculté',string)
