import os
import numpy as np
import matplotlib.pyplot as plt
import dask.dataframe as dd
from moveminer.utils.config import col_names


def generate_cde_plot(
    df, category_column, value_column, label, output_folder="output"
):
    output_path = f"assets/{output_folder}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for cat in df[category_column].unique():
        # Filtra os dados para a categoria atual
        filtered_df = df[df[category_column] == cat]
        # Verifica se a pasta de saída existe, se não, cria

        # Plota o gráfico CDE
        data_sorted = np.sort(filtered_df[value_column].values)

        # Get cumulative probabilities
        cumulative = np.arange(1, len(data_sorted) + 1) / len(data_sorted)

        # Plot
        plt.plot(data_sorted, cumulative)
        plt.xlabel(label)
        plt.ylabel("Cumulative Probability")
        plt.title(f"{category_column} - {cat}")
        plt.grid(True)
        cat = str(cat).replace("/", "_")
        plt.savefig(
            f"{output_path}/{category_column}_{cat}_cde.png",
            dpi=300,
        )
        plt.savefig(
            f"{output_path}/{category_column}_{cat}_cde.pdf",
            dpi=300,
        )
        plt.close()


def main(df, categories, columns):
    # Exemplo de uso
    for cat in categories:
        for val in columns:
            generate_cde_plot(
                df,
                category_column=cat,
                value_column=val["column"],
                label=val["label"],
                output_folder=val["column"],
            )


if __name__ == "__main__":
    # Carrega os dados
    points = dd.read_csv("./anglova/enriched_anglova.csv").compute()
    # # Exemplo de uso
    # main(
    #     points,
    #     [
    #         "Company",
    #         "Company Type",
    #         "Platoon",
    #         "Platoon Type",
    #         "Vehicle Function",
    #         "Vehicle Type",
    #         "Command",
    #     ],
    #     [
    #         {"column": col_names.SPEED, "label": "Speed (m/s)"},
    #         {"column": col_names.ACCELERATION, "label": "Acceleration (m/s²)"},
    #         {"column": col_names.DISTANCE, "label": "Distance (m)"},
    #         {"column": col_names.DELTA_TIME, "label": "Delta Time (s)"},
    #     ],
    # )
