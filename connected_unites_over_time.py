import os

import dask.dataframe as dd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_connected_units_per_second(
    pairwise_distances,
    enriched_trajectories_df,
    connection_type="Bluetooth",
    category="Company",
    ecdf=False,
):
    # Filtrar apenas as linhas onde Bluetooth é verdadeiro
    connection_true = pairwise_distances[pairwise_distances[connection_type]]

    # Agrupar por segundo e calcular o número de IDs únicos
    connected_devices_per_second = (
        connection_true.groupby("t")
        .apply(
            lambda x: pd.Series(
                {
                    "unique_count": len(
                        pd.unique(x[["id1", "id2"]].values.ravel())
                    ),
                    "unique_ids": pd.unique(
                        x[["id1", "id2"]].values.ravel()
                    ).tolist(),
                }
            )
        )
        .reset_index()
    )

    # Create a mapping of trajectory_id to Company
    trajectory_to_company = enriched_trajectories_df.set_index(
        "trajectory_id"
    )[category].to_dict()

    # For each unique Company, add a new column to connected_devices_per_second
    for company in enriched_trajectories_df[category].unique():
        connected_devices_per_second[f"{category}_{company}"] = (
            connected_devices_per_second["unique_ids"].apply(
                lambda ids: sum(
                    trajectory_to_company.get(id_, None) == company
                    for id_ in ids
                )
            )
        )

    # Plotting
    plt.figure(figsize=(12, 6))
    for company in enriched_trajectories_df[category].unique():
        x = f"{category}_{company}"
        label = company
        if ecdf:
            sns.ecdfplot(
                data=connected_devices_per_second,
                x=x,
                label=label,
            )
            continue
        plt.plot(
            connected_devices_per_second["t"],
            connected_devices_per_second[x],
            label=label,
        )
    plt.xlabel("Time (t)" if not ecdf else "Number of Connected Units")
    plt.ylabel("Number of Connected Units" if not ecdf else "Density")
    plt.title(f"{category} - {connection_type} Connected Units Per Second")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # Save the plot
    output_path = f"assets2/{connection_type}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    sufix = "_ecdf" if ecdf else ""
    plt.savefig(
        f"{output_path}/{category}{sufix}.png",
        dpi=300,
    )
    plt.savefig(
        f"{output_path}/{category}{sufix}.pdf",
        dpi=300,
    )
    plt.close()


if __name__ == "__main__":
    pairwise_distances = dd.read_csv(
        "./pairwise_distances.csv",
        parse_dates=["t"],
    ).compute()
    enriched_trajectories_df = pd.read_csv(
        "./anglova_metrics_enriched/trajectories_enriched_metrics.csv",
    )

    pairwise_distances["Bluetooth"] = (
        pairwise_distances["distance"] <= 0.01
    )  # 10m
    pairwise_distances["Wi-Fi"] = (
        pairwise_distances["distance"] <= 0.15
    )  # 150m
    pairwise_distances["UHF"] = pairwise_distances["distance"] <= 2  # 2km
    pairwise_distances["VHF"] = pairwise_distances["distance"] <= 20  # 20km

    connection_types = ["Bluetooth", "Wi-Fi", "UHF", "VHF"]
    categories = [
        "Company",
        "Company Type",
        "Platoon",
        "Platoon Type",
        "Vehicle Function",
        "Vehicle Type",
        "Command",
    ]
    for ecdf in [False, True]:
        for connection_type in connection_types:
            for category in categories:
                plot_connected_units_per_second(
                    pairwise_distances,
                    enriched_trajectories_df,
                    connection_type=connection_type,
                    category=category,
                    ecdf=ecdf,
                )
