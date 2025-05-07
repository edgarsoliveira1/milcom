import os

import dask.dataframe as dd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    # Carrega os dados
    enriched_points = dd.read_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv",
    ).compute()
    enriched_points["t"] = pd.to_datetime(enriched_points["t"])
    enriched_points["t"] = enriched_points["t"].dt.strftime("%H:%M:%S")
    enriched_trajectories_df = pd.read_csv(
        "./anglova_metrics_enriched/trajectories_enriched_metrics.csv",
    )
    plt.rcParams.update({"font.size": 24})
    mean_speed_per_second = enriched_points.groupby("t")["speed"].mean()
    mean_speed_per_second.rolling(window=100, center=True).mean().plot(
        figsize=(12, 6), xlabel="Time", ylabel="Mean Speed"
    )
    plt.xticks(rotation=45)
    # mean_speed_per_second.plot(xlabel="Time", ylabel="Mean Speed")
    # Verifica se a pasta de saída existe, se não, cria
    OUTPUT_PATH = "./assets/Speed Over Time/"
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    # Salva o arquivo
    plt.savefig(
        f"{OUTPUT_PATH}/Anglova.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.savefig(
        f"{OUTPUT_PATH}/Anglova.pdf",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()
    for hue in [
        "Company",
        "Company Type",
        "Platoon",
        "Platoon Type",
        "Vehicle Function",
        "Vehicle Type",
        "Command",
    ]:
        mean_speed_per_second = (
            enriched_points.groupby(["t", hue])["speed"].mean().unstack()
        )
        mean_speed_per_second.rolling(window=100, center=True).mean().plot(
            figsize=(12, 6),
            xlabel="Time",
            ylabel="Mean Speed",
        )
        plt.xticks(rotation=45)

        # mean_speed_per_second.plot(xlabel="Time", ylabel="Mean Speed")
        # Verifica se a pasta de saída existe, se não, cria
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        # Salva o arquivo
        plt.savefig(
            f"{OUTPUT_PATH}/{hue}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.savefig(
            f"{OUTPUT_PATH}/{hue}.pdf",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()
