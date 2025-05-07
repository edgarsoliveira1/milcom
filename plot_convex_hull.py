import os

import contextily as ctx
import dask.dataframe as dd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.spatial import ConvexHull


def plot_convex_hull(df, category, output_path):
    if category:
        unique_categories = df[category].unique()

    plt.figure(figsize=(12, 8))
    if not category:
        points = df[["x", "y"]].dropna().values
        plt.plot(
            points[:, 0],
            points[:, 1],
            "o",
            markersize=2,
            label="Points",
        )
    anglova_points = df[["x", "y"]].dropna().values
    anglova_hull = ConvexHull(anglova_points)
    anglova_hull_points = anglova_points[anglova_hull.vertices]
    plt.plot(
        np.append(anglova_hull_points[:, 0], anglova_hull_points[0, 0]),
        np.append(anglova_hull_points[:, 1], anglova_hull_points[0, 1]),
        "-",
        label="Anglova",
    )
    if category:
        for cat in unique_categories:
            # Filtra os pontos para a empresa atual
            cat_points = df[df[category] == cat][["x", "y"]].dropna().values

            if len(cat_points) < 3:
                # ConvexHull precisa de pelo menos 3 pontos
                continue

            # Calcula o ConvexHull
            cat_hull = ConvexHull(cat_points)
            cat_hull_points = cat_points[cat_hull.vertices]

            # Plota os pontos e o ConvexHull
            # plt.plot(company_points[:, 0], company_points[:, 1], 'o',
            # markersize=2, label=f'Company {company} Points')
            plt.plot(
                np.append(cat_hull_points[:, 0], cat_hull_points[0, 0]),
                np.append(cat_hull_points[:, 1], cat_hull_points[0, 1]),
                "--",
                linewidth=10,
                label=cat,
            )
            if not category:
                plt.fill(
                    cat_hull_points[:, 0], cat_hull_points[:, 1], alpha=0.2
                )

    # Configurações do gráfico
    if category == "Command":
        handles, labels = plt.gca().get_legend_handles_labels()
        if len(labels) > 4:
            handles = [handles[0]] + handles[-3:]
            labels = [labels[0]] + labels[-3:]
        plt.legend(handles, labels, fontsize=24, loc="upper right")
    else:
        plt.legend(fontsize=24, loc="upper right")
    ax = plt.gca()
    ax.axis("off")
    ctx.add_basemap(
        ax,
        crs="EPSG:4326",
        source=ctx.providers.CartoDB.Positron,
    )
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # Salva o arquivo
    filename = f"{category if category else 'Anglova'}"
    plt.savefig(
        f"{output_path}/{filename}.png",
        bbox_inches="tight",
    )
    plt.savefig(
        f"{output_path}/{filename}.pdf",
        bbox_inches="tight",
    )
    plt.show()


if __name__ == "__main__":
    # Carrega os dados
    enriched_points = dd.read_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv",
    ).compute()
    enriched_points["t"] = pd.to_datetime(enriched_points["t"])
    enriched_trajectories_df = pd.read_csv(
        "./anglova_metrics_enriched/trajectories_enriched_metrics.csv",
    )
    output_path = "./assets/Convex Hull/"
    # for category in [
    #     None,
    #     "Company",
    #     "Company Type",
    #     "Platoon",
    #     "Platoon Type",
    #     "Vehicle Function",
    #     "Vehicle Type",
    #     "Command",
    # ]:
    #     plot_convex_hull(enriched_points, category, output_path)

    # df = enriched_points
    # CATEGORY = "Company"
    # unique_categories = df[CATEGORY].unique()
    # plt.figure(figsize=(12, 8))
    # anglova_points = df[["x", "y"]].dropna().values
    # anglova_hull = ConvexHull(anglova_points)
    # anglova_hull_points = anglova_points[anglova_hull.vertices]
    # plt.plot(
    #     np.append(anglova_hull_points[:, 0], anglova_hull_points[0, 0]),
    #     np.append(anglova_hull_points[:, 1], anglova_hull_points[0, 1]),
    #     "-",
    #     label="Anglova",
    # )
    # for cat in unique_categories:
    #     # Filtra os pontos para a empresa atual
    #     cat_points = df[df[CATEGORY] == cat][["x", "y"]].dropna().values

    #     if len(cat_points) < 3:
    #         # ConvexHull precisa de pelo menos 3 pontos
    #         continue

    #     # Calcula o ConvexHull
    #     cat_hull = ConvexHull(cat_points)
    #     cat_hull_points = cat_points[cat_hull.vertices]

    #     # Plota os pontos e o ConvexHull
    #     # plt.plot(company_points[:, 0], company_points[:, 1], 'o',
    #     # markersize=2, label=f'Company {company} Points')
    #     plt.plot(
    #         np.append(cat_hull_points[:, 0], cat_hull_points[0, 0]),
    #         np.append(cat_hull_points[:, 1], cat_hull_points[0, 1]),
    #         "--",
    #         linewidth=10,
    #         label=f"Company {cat}",
    #     )
    # plt.legend(fontsize=24, loc="upper right")
    # ax = plt.gca()
    # ax.axis("off")
    # ctx.add_basemap(
    #     ax,
    #     crs="EPSG:4326",
    #     source=ctx.providers.CartoDB.Positron,
    # )
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    # # Salva o arquivo
    # FILENAME = f"{CATEGORY if CATEGORY else 'Anglova'}"
    # plt.savefig(
    #     f"{output_path}/{FILENAME}.png",
    #     bbox_inches="tight",
    # )
    # plt.savefig(
    #     f"{output_path}/{FILENAME}.pdf",
    #     bbox_inches="tight",
    # )
    # plt.show()
    # Command
    df = enriched_points
    CATEGORY = "Command"
    unique_categories = df[CATEGORY].unique()

    unique_categories = df[CATEGORY].unique()
    plt.figure(figsize=(12, 8))
    anglova_points = df[["x", "y"]].dropna().values
    anglova_hull = ConvexHull(anglova_points)
    anglova_hull_points = anglova_points[anglova_hull.vertices]
    plt.plot(
        np.append(anglova_hull_points[:, 0], anglova_hull_points[0, 0]),
        np.append(anglova_hull_points[:, 1], anglova_hull_points[0, 1]),
        "-",
        label="Anglova",
    )
    # Combine categories below 5% into a single category
    category_counts = df[CATEGORY].value_counts(normalize=True)
    small_categories = category_counts[category_counts < 0.02].index
    # df[CATEGORY] = df[CATEGORY].apply(
    #     lambda x: "Others" if x in small_categories else x
    # )
    df = df[df[CATEGORY].isin(small_categories)]
    for cat in unique_categories:
        # Filtra os pontos para a empresa atual
        cat_points = df[df[CATEGORY] == cat][["x", "y"]].dropna().values

        if len(cat_points) < 3:
            # ConvexHull precisa de pelo menos 3 pontos
            continue

        # Calcula o ConvexHull
        cat_hull = ConvexHull(cat_points)
        cat_hull_points = cat_points[cat_hull.vertices]

        # Plota os pontos e o ConvexHull
        # plt.plot(company_points[:, 0], company_points[:, 1], 'o',
        # markersize=2, label=f'Company {company} Points')
        color = plt.cm.Dark2(unique_categories.tolist().index(cat) / len(unique_categories))
        plt.plot(
            np.append(cat_hull_points[:, 0], cat_hull_points[0, 0]),
            np.append(cat_hull_points[:, 1], cat_hull_points[0, 1]),
            "--",
            linewidth=10,
            label=cat,
            color=color,
        )
    plt.legend(fontsize=24, loc="upper right")
    ax = plt.gca()
    ax.axis("off")
    # Extend the bounding box of the plot
    ax.set_xlim(
        ax.get_xlim()[0],
        ax.get_xlim()[1] + 0.3 * (ax.get_xlim()[1] - ax.get_xlim()[0]),
    )
    ax.set_ylim(
        ax.get_ylim()[0],
        ax.get_ylim()[1] + 0.3 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
    )
    ctx.add_basemap(
        ax,
        crs="EPSG:4326",
        source=ctx.providers.CartoDB.Positron,
    )

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # Salva o arquivo
    FILENAME = f"{CATEGORY if CATEGORY else 'Anglova'}"
    plt.savefig(
        f"{output_path}/{FILENAME}.png",
        bbox_inches="tight",
    )
    plt.savefig(
        f"{output_path}/{FILENAME}.pdf",
        bbox_inches="tight",
    )
    plt.show()
