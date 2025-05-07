import os

import contextily as ctx
import dask.dataframe as dd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_spatiotemporal_coverage(df, category, output_dir):
    # Criar GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.x, df.y), crs="EPSG:4326"
    )
    gdf = gdf.to_crs(
        epsg=3857
    )  # Projeção para mapas da Web (compatível com contextily)

    # Obtém os limites do GeoDataFrame (em EPSG:3857)
    bbox = gdf.total_bounds  # [minx, miny, maxx, maxy]

    # Calcula a margem (5% do tamanho em cada eixo)
    margin_x = (bbox[2] - bbox[0]) * 0.05
    margin_y = (bbox[3] - bbox[1]) * 0.05

    # Aplica a margem aos limites
    minx = bbox[0] - margin_x
    maxx = bbox[2] + margin_x
    miny = bbox[1] - margin_y
    maxy = bbox[3] + margin_y

    # Adjusting subplot dimensions and stretching images
    fig, axes = plt.subplots(nrows=3, ncols=8, figsize=(16, 12), dpi=300)
    axes = axes.flatten()

    unique_t = df["t"].unique()
    # Selecionar 24 valores únicos de 't' com espaçamento uniforme
    selected_t = unique_t[np.linspace(0, len(unique_t) - 1, 24, dtype=int)]

    for i, st in enumerate(selected_t):
        ax = axes[i]

        # Filtrar por hora
        gdf_s = gdf[gdf["t"] == st]

        if not gdf_s.empty:
            if category is not None:
                gdf_s.plot(
                    ax=ax,
                    column=category,
                    legend=False,
                    markersize=5,
                    cmap="viridis",
                )
            else:
                gdf_s.plot(ax=ax, color="red", markersize=5)

        # Ajustar mapa
        ax.set_title(
            st.strftime("%H:%M:%S"), fontsize=24, backgroundcolor="#cccccc"
        )
        ax.legend()
        ax.axis("off")
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.set_aspect("auto")  # Stretch images to fill subplot space

        # Adicionar background
        try:
            ctx.add_basemap(
                ax,
                crs=gdf_s.crs.to_string(),
                source=ctx.providers.CartoDB.Positron,
                attribution_size=2,
            )
        except (ValueError, KeyError, TypeError):
            pass  # caso não haja pontos nessa hora

    # Título geral
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    # Verifica se a pasta de saída existe, se não, cria
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Salva o arquivo
    plt.savefig(
        f"{output_dir}/{category}.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.savefig(
        f"{output_dir}/{category}.pdf",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)


if __name__ == "__main__":
    enriched_points = dd.read_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv",
    ).compute()
    enriched_points["t"] = pd.to_datetime(enriched_points["t"])
    output_folder = "./assets/Spatiotemporal Coverage/"
    categorias = [
        None,
        # "Company",
        # "Company Type",
        # "Platoon",
        # "Platoon Type",
        # "Vehicle Function",
        # "Vehicle Type",
        # "Command",
    ]
    for cat in categorias:
        plot_spatiotemporal_coverage(
            enriched_points,
            category=cat,
            output_dir=output_folder,
        )
