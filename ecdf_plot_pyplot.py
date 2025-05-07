import os

import dask.dataframe as dd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from moveminer.utils.config import col_names


def main(df, categories, columns):
    # Remove duplicatas no DataFrame

    # Exemplo de uso
    for cat in categories:
        for val in columns:
            print(f"Gerando gráfico de densidade para {cat} - {val['label']}")
            # Configura o tamanho da figura
            plt.figure(figsize=(12, 6))

            # Cria o gráfico de densidade
            sns.ecdfplot(
                data=df.dropna(subset=[val["column"]]),
                x=val["column"],
                hue=cat,
                # fill=True,
                # common_norm=False,
                palette="tab10",
            )

            # Configurações do gráfico
            plt.xlabel(val["label"])
            plt.ylabel("Density")
            plt.title(f"{cat} - {val['label']}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            output_path = f"assets2/{val['column']}"
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            cat = str(cat).replace("/", "_")
            plt.savefig(
                f"{output_path}/{cat}_{val['column']}_ecdf.png",
                dpi=300,
            )
            plt.savefig(
                f"{output_path}/{cat}_{val['column']}_ecdf.pdf",
                dpi=300,
            )
            plt.close()


if __name__ == "__main__":
    # Carrega os dados
    enriched_points = dd.read_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv",
    ).compute()
    enriched_trajectories_df = pd.read_csv(
        "./anglova_metrics_enriched/trajectories_enriched_metrics.csv",
    )
    anglova_categories = [
        "Company",
        "Company Type",
        "Platoon",
        "Platoon Type",
        "Vehicle Function",
        "Vehicle Type",
        "Command",
    ]
    point_metrics = [
        {"column": col_names.SPEED, "label": "Speed (km/h)"},
        {"column": col_names.ACCELERATION, "label": "Acceleration (km/h²)"},
        {"column": col_names.DISTANCE, "label": "Distance (km)"},
        {"column": col_names.DELTA_TIME, "label": "Delta Time (h)"},
    ]
    trajectory_metrics = [
        # {"column": col_names.TOTAL_DISTANCE, "label": "Total Distance (km)"},
        # {
        #     "column": col_names.STRAIGHT_LINE_DISTANCE,
        #     "label": "Straight Line Distance (km)",
        # },
        # {"column": col_names.PATH_TORTUOSITY, "label": "Path Tortuosity (km)"},
        # {
        #     "column": col_names.RADIUS_GYRATION,
        #     "label": "Radius of Gyration (km)",
        # },
        # {"column": col_names.TIME_STOPPED, "label": "Time Stopped (h)"},
        {"column": col_names.DESTINE_ARRIVE_TIME, "label": "Destine Arrive Time"},
    ]
    # Exemplo de uso
    # main(
    #     enriched_points,
    #     anglova_categories,
    #     point_metrics,
    # )
    enriched_trajectories_df[col_names.DESTINE_ARRIVE_TIME] = pd.to_datetime(
        enriched_trajectories_df[col_names.DESTINE_ARRIVE_TIME]
    )
    main(
        enriched_trajectories_df,
        anglova_categories,
        trajectory_metrics,
    )

