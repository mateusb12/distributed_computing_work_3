import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CSV_FILE = ("C:\\Users\\Mateus\\Desktop\\unifor\\computacao_distribuida\\docker_unifor\\final_results\\"
            "csvs\\merged_history.csv")
AGGREGATE_FUNCTION = 'median'


def create_chart(input_df, y_value_column, y_label, title, colors):
    pivot_table = input_df[input_df['User Count'].isin([10, 100, 1000])].pivot_table(
        index='User Count', columns='Containers',
        values=y_value_column, aggfunc=AGGREGATE_FUNCTION).reset_index()

    labels = pivot_table['User Count'].tolist()
    width = 0.20
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(10, 6))

    for idx, container_count in enumerate(pivot_table.columns[1:]):
        ax.bar(x + idx * width, pivot_table[container_count].tolist(), width,
               label=f'{container_count} instância(s)', color=colors[idx], edgecolor='black', zorder=3)

    ax.set_xlabel('Número de usuários')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x + width)
    ax.set_xticklabels(labels)
    ax.legend(loc="upper left")
    ax.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)

    fig.tight_layout()
    plt.show()


def response_time_chart(input_df):
    colors = ['#cfe2f3', '#fce5cd', '#f4cccc']
    create_chart(input_df, 'Total Average Response Time', 'Tempo de resposta (ms)',
                 'Tempo médio de resposta vs número de usuários', colors)


def requisitions_per_second_chart(input_df):
    colors = ['#d9ead3', '#d0e0e3', '#fff2cc']
    create_chart(input_df, 'Requests/s', 'Requisições por segundo',
                 'Requisições por segundo vs número de usuários', colors)


def __main():
    df = pd.read_csv(CSV_FILE)
    response_time_chart(input_df=df)
    requisitions_per_second_chart(input_df=df)


if __name__ == "__main__":
    __main()
