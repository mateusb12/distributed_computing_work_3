import os
import shutil

import pandas as pd
CSV_PATH = "C:\\Users\\Mateus\\Desktop\\unifor\\computacao_distribuida\\docker_unifor\\final_results\\csvs"


def __extract_info_from_filename(filename):
    split_name = filename.split('_')
    users = int(split_name[1])
    instances = int(split_name[3])
    return users, instances


def __add_info_to_dfs(files):
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        users, instances = __extract_info_from_filename(file)
        df['Users'] = users
        df['Containers'] = instances
        dfs.append(df)
    return dfs


def load_and_merge_all_csvs():
    os.chdir(CSV_PATH)
    all_files = os.listdir(CSV_PATH)

    exception_files = [file for file in all_files if file.endswith("exceptions.csv")]
    failures_files = [file for file in all_files if file.endswith("failures.csv")]
    stats_files = [file for file in all_files if file.endswith("stats.csv")]
    history_files = [file for file in all_files if file.endswith("history.csv")]

    exception_dfs = __add_info_to_dfs(exception_files)
    failures_dfs = __add_info_to_dfs(failures_files)
    stats_dfs = __add_info_to_dfs(stats_files)
    history_dfs = __add_info_to_dfs(history_files)

    merged_exception = pd.concat(exception_dfs)
    merged_failures = pd.concat(failures_dfs)
    merged_stats = pd.concat(stats_dfs)
    merged_history = pd.concat(history_dfs)

    merged_exception.to_csv("merged_exceptions.csv", index=False)
    merged_failures.to_csv("merged_failures.csv", index=False)
    merged_stats.to_csv("merged_stats.csv", index=False)
    merged_history.to_csv("merged_history.csv", index=False)

    old_data_path = os.path.join(CSV_PATH, "old_data")
    if not os.path.exists(old_data_path):
        os.makedirs(old_data_path)

    for file in exception_files + failures_files + stats_files + history_files:
        shutil.move(file, os.path.join(old_data_path, file))
    return True


def __main():
    aux = load_and_merge_all_csvs()


if __name__ == "__main__":
    __main()
