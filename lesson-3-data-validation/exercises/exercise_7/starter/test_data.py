import pytest
import wandb
import pandas as pd

# This is global so all tests are collected under the same
# run
run = wandb.init(project="exercise_7", job_type="data_tests")


@pytest.fixture(scope="session")
def data():

    local_path = run.use_artifact("exercise_5/preprocessed_data:latest").file()
    df = pd.read_csv(local_path, low_memory=False)

    return df


def test_column_presence_and_type(data):

    # A dictionary with the column names as key and a function that verifies
    # the expected dtype for that column. We do not check strict dtypes (like
    # np.int32 vs np.int64) but general dtypes (like is_integer_dtype)
    required_columns = {
        "time_signature": pd.api.types.is_integer_dtype,
        "key": pd.api.types.is_integer_dtype,
        "danceability": pd.api.types.is_float_dtype,
        "energy": pd.api.types.is_float_dtype,
        "loudness": pd.api.types.is_float_dtype,
        "speechiness": pd.api.types.is_float_dtype,
        "acousticness": pd.api.types.is_float_dtype,
        "instrumentalness": pd.api.types.is_float_dtype,
        "liveness": pd.api.types.is_float_dtype,
        "valence": pd.api.types.is_float_dtype,
        "tempo": pd.api.types.is_float_dtype,
        "duration_ms": pd.api.types.is_integer_dtype,  # This is integer, not float as one might expect
        "text_feature": pd.api.types.is_string_dtype,
        "genre": pd.api.types.is_string_dtype
    }

    # Check column presence
    assert set(data.columns.values).issuperset(set(required_columns.keys()))

    # Check that the columns are of the right dtype
    for col_name, format_verification_funct in required_columns.items():

        assert format_verification_funct(data[col_name]), f"Column {col_name} failed test {format_verification_funct}"


def test_class_names(data):
    known_classes = [
        "Dark Trap",
        "Underground Rap",
        "Trap Metal",
        "Emo",
        "Rap",
        "RnB",
        "Pop",
        "Hiphop",
        "techhouse",
        "techno",
        "trance",
        "psytrance",
        "trap",
        "dnb",
        "hardstyle",
    ]
    # Check that the genre column has only the expected class names
    assert set(data["genre"]).issuperset(set(known_classes))

def test_column_ranges(data):

    # A dictionary with the column names as key and a function that verifies
    # the expected range for that column. We do not check strict ranges (like
    # np.int32 vs np.int64) but general ranges (like is_integer_dtype)
    ranges = {
        "time_signature": (1, 5),
        "key": (0, 11),
        "danceability": (0, 1),
        "energy": (0, 1),
        "loudness": (-35, 5),
        "speechiness": (0, 1),
        "acousticness": (0, 1),
        "instrumentalness": (0, 1),
        "liveness": (0, 1),
        "valence": (0, 1),
        "tempo": (50, 250),
        "duration_ms": (20000, 1000000),
    }

    # Check column ranges
    for col_name, range_verification_funct in ranges.items():

        assert data[col_name].dropna().between(*range_verification_funct).all(), f"Column {col_name} failed test {range_verification_funct}"

