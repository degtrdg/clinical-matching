import pandas as pd
import pickle
import numpy as np
import traceback
from os.path import isfile, join
from os import listdir
import os


def process_geodata(directory, clust_dict):
    y_val = pd.DataFrame()
    x_val = pd.DataFrame()

    dict = open_file(clust_dict)
    sample_names = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        df = pd.read_csv(file_path, sep=",", header=0, index_col=0)

        cancer_name = (
            get_cancer_acronym(filename.split("_")[0]) if "_" in filename else None
        )

        if cancer_name:
            df = get_data(df, dict, name=cancer_name, output=True, save=False)

            # Updating y_val
            df_y = df.copy()
            df_y[cancer_name] = (~df_y.index.str.contains("n")).astype(int)
            df_y["Normal"] = (df_y.index.str.contains("n")).astype(int)
            df_y = df_y[[cancer_name, "Normal"]]
            y_val = pd.concat([y_val, df_y])

            # Updating x_val
            x_val = pd.concat([x_val, df])

    y_val = y_val.fillna(0)
    x_val = x_val.fillna(0)

    # Save y_val and x_val to pickle files
    print(y_val)
    print(x_val)
    y_val.to_pickle("y_val.pickle")
    x_val.to_pickle("x_val.pickle")


def get_cancer_acronym(experiment_number):
    """
    Given an experiment number, return the corresponding cancer acronym.

    :param experiment_number: A string representing the experiment number.
    :return: A string representing the cancer acronym.
    """
    mapping = {
        "GSE54719": "NB",
        "GSE59157": "WT",
        "GSE62298": "AML",
        "GSE113501": "RCC",
    }

    return mapping.get(experiment_number, "Unknown")


def make_name(prefix, suffix, filetype):
    """generates filenames or filepaths
    if dots or slashes separate the three parts they must be included in the text of one of the parts
    prefix may be a filepath
    suffix may be the filename
    filetype is the type of file

    """
    name = prefix + suffix + filetype
    return name


def mark_normals(sample_df):
    mask = sample_df.index.str.contains("11")  # Find rows where index contains '11'
    sample_df.loc[
        mask, sample_df.columns[2]
    ] = 33  # Set third column value to 33 in those rows
    return sample_df


def sep_normals(sample_df):
    # Create a boolean mask for rows where the index doesn't contain '11'
    mask = sample_df.index.str.contains("11")
    # Apply the mask to the DataFrame to keep only the rows where the first column doesn't contain '11'
    sample_df2 = sample_df[mask]
    return sample_df2


def check_normal(row):
    # Extract the last number in the 'Sample ID'
    last_number = int(row.name.split("-")[-1][:-1])
    # If the number is greater than 10, set all values to 0 and 'Normal' to 1
    if last_number >= 10:
        row.loc[:] = 0
        row["Normal"] = 1
    return row


def get_x_vals(sample_df):
    mask = ~sample_df.index.str.contains("11")
    sample_df2 = sample_df[mask]
    return sample_df2


def rename_cols(data, row_name):
    """data must be a pandas DataFrame
    renames columns with the values in a given row
    rows may not be referenced by row/index number unless the number is also the name of the row
    """
    columns = data.loc[row_name]
    data.columns = columns
    return data


def assemble_x(names, pathway=False, reshuffle=False):
    """takes the names provided and opens the .pickle files associated with that name
    pathway is a boolean to declare that the names are a full pathway"""
    if pathway == False:
        p = picklefy(names)
    else:
        p = names
    d = list()
    for i in p:
        d.append(open_file(i))
    data = pd.concat(d)
    if reshuffle == True:
        data = data.sample(frac=1)
    return data


def picklefy(names):
    p = list()
    for i in names:
        p.append(i + ".pickle")
    return p


def save_file(data, name):
    """can save files as csv or in pickle format.
    pickle is preferred as it is faster
    csv save must have data in a pandas DataFrame
    """
    filetype = name.split(".")[-1]
    assert (
        filetype == "pickle"
        or filetype == "csv"
        or filetype == "txt"
        or filetype == "pkl"
        or filetype == "sampleMap_HumanMethylation450"
    ), "filetype must be 'pickle', or 'csv'"
    if filetype == "pkl":
        with open(name, "wb") as handle:
            pickle.dump(data, handle)
    if filetype == "pickle":
        with open(name, "wb") as handle:
            pickle.dump(data, handle)
    if filetype == "csv":
        assert (
            type(data) == pd.DataFrame
        ), "to save as 'csv' please ensure the data is a pandas DataFrame"
        data.to_csv(name)


def open_file(filename, sep=",", header=0, index_col=None, rename=None):
    """opens a file.
    Capable of opening pickle, csv or txt formats
    for csvs or txt the separator must be indicated
    if a specific index should be used as the column names then index_col may be used and must be the index number
    if index number is unknown but index name is then rename will take the index name and do the same thing as index_col
    """
    # from pandas.io.parser import CParserError

    filetype = filename.split(".")[-1]
    assert (
        filetype == "pickle"
        or filetype == "csv"
        or filetype == "txt"
        or filetype == "pkl"
        or filetype == "sampleMap_HumanMethylation450"
    ), "filetype must be 'pickle', txt' or 'csv'"
    if filetype == "pkl":
        data = pd.read_pickle(filename)
    if filetype == "pickle":
        with open(filename, "rb") as handle:
            data = pickle.load(handle)

    if filetype == "csv":
        # assert type(data) == pd.DataFrame, "to open a 'csv' please ensure the data is a pandas DataFrame"
        data = pd.read_csv(filename, sep=sep, header=header, index_col=index_col)

    if filetype == "txt":
        data = pd.read_csv(filename, sep=sep, header=header, index_col=index_col)
    if filetype == "sampleMap_HumanMethylation450":
        data = pd.read_csv(filename, sep=sep, header=header, index_col=index_col)
        #     except FileNotFoundError:
        #         name_parts = filename.split("_")
        #         filename = name_parts[0]+"-GPL13534_"+name_parts[1]+"_"+name_parts[2]
        #         try:
        #             data = pd.DataFrame.from_csv(filename, sep = sep, header = header, index_col = index_col)

        #         except CParserError:
        #             handler = False
        #             while not handler:
        #                 header+=1
        #                 handler, data = ErrorHandler(filename, header, sep, index_col)

        #     except CParserError:
        #         handler = False
        #         while not handler:
        #             header+=1
        #             handler, data = ErrorHandler(filename, header, sep, index_col)
        if rename != None:
            data = rename_cols(data, row_name)
    return data


def get_data(data, probes, name="", output=True, save=True, split_name=False):
    """
    returns a DataFrame with columns being the cpg islands and rows being samples
    Data is a DataFrame of beta values with the cpg id's as the row names and sample names as column names
    probes is a dictionary with chromosomes as keys and a dict as value. The second level dict has
    chromosome cluster names as keys (such as chr1.1) and the specific cpg ids as values.
    The second level keys will become the column names of the output DataFrame
    If you want to autosave then name should be a unique name for the output file.
    This is highly reccomended so that multiple runs of this function are not required
    If you do not want to save then save should be set to False
    output being set to true will return the DataFrame as output.
    if you only want to generate the file without an output in the session set this to False and save to True
    for multiple files at a time you may run this function inside a loop
    """

    data_dict = dict()
    l = len(data.columns)
    cols = list()
    time = 0
    for c in probes.keys():
        for i in probes[c].keys():
            if not time:
                cols.append(i)
            try:
                data_i = data.loc[probes[c][i]].mean(axis=0)
                data_dict.setdefault(i, data_i)
            except:
                data_dict.setdefault(i, pd.Series([0] * l, index=data.columns))
                traceback.print_exc()

        print(c, end=" ")
    time += 1
    data_dict = pd.DataFrame.from_dict(data_dict, orient="columns")
    data_dict = data_dict.reindex(columns=cols)
    if save:
        if split_name:
            name = make_name(
                prefix=name.split("_")[0].split("-")[0],
                suffix="_AVGS",
                filetype=".pickle",
            )
        save_file(data_dict, name)

    if output:
        return data_dict


def clean(x, y):
    print(x.shape)

    todrop = [
        "submitter_id",
        "entity_type",
        "entity_id",
        "category",
        "classification",
        "created_datetime",
        "status",
        "notes",
        "annotations",
    ]
    x.drop(todrop, inplace=True)
    y.drop(todrop, inplace=True)
    mask = x.index.isnull()
    x = x[mask]
    mask = y.index.isnull()
    y = y[mask]
    print(x.shape)


def match_samples(x, y, dir):
    dfs = []
    for folder in os.listdir(dir):
        if "gz" not in folder:
            folder = os.path.join(dir, folder)
            for file in os.listdir(folder):
                file = os.path.join(folder, file)
                if "sample_sheet" in file:
                    print(file)
                    df = pd.read_csv(file, sep="\t")
                    df["File ID"] = df["File Name"].apply(lambda x: x.split(".")[0])
                    dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)

    id_dict = df.set_index("File ID")["Sample ID"].to_dict()
    # print(id_dict)
    # print(id_dict.get("547a2572-97d1-4496-9953-6a7a97d7eb75"))
    x = x.index.map(id_dict)
    y.index = y.index.map(id_dict)
    # print(y)


def semanticClustering():
    return


"""    sample_names = []
    for cancer in os.listdir(dir):
        if "gz" not in cancer:
            cancer = os.path.join(dir, cancer)
            for folder in os.listdir(cancer):
                if ".txt" not in folder and ".tsv" not in folder:
                    folder = os.path.join(cancer, folder)
                    file = os.listdir(folder)[0]
                    sample_names.append(file.split(".")[0])"""


"""
data = pd.read_csv(
    "/work/08560/danyang/DiseaseNet/Data_2023/TCGA/TCGA.SARC.sampleMap_HumanMethylation450",
    sep="\t",
    header=0,
    index_col=0
)
"""
# print(y)

# x.drop("annotations", inplace=True)
# y.drop("annotations", inplace=True)


# clean(x, y)


# print(x.index)
# match_samples(x, y, "/work/08560/danyang/DXNet/data_pipeline/TCGA")

# y["Normal"] = 0
# y = y.apply(check_normal, axis=1)


# x.to_pickle("x_final.pickle")
# y.to_pickle("y_final.pickle")

# print(y)
# df = pd.read_pickle("C:\\Users\\joewc\\OneDrive\\Desktop\\CancerResearch\\Data_2023\\SARC_AVGS.pickle")
# df = mark_normals(df)


# print(df.shape)
