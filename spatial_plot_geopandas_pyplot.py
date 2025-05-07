import os
import time

import contextily as ctx
import dask.dataframe as dd
import geopandas as gpd
import matplotlib.cm as cm
import matplotlib.pyplot as plt


def highlight_first_last_points(ax, gpd):
    # Define os pontos iniciais e finais
    start_points = gpd.groupby("id").first()
    end_points = gpd.groupby("id").last()
    # Plota os pontos iniciais e finais
    ax.scatter(
        start_points.geometry.x,
        start_points.geometry.y,
        color="#32CD32",
        marker="o",
        label="Start",
        s=10,
        zorder=3,
    )
    ax.scatter(
        end_points.geometry.x,
        end_points.geometry.y,
        color="#FF4500",
        marker="X",
        label="End",
        s=10,
        zorder=3,
    )
    ax.legend(loc="upper right", fontsize=8)


def generate_spatial_plots(
    df,
    category_column,
    output_folder="output",
    highlight_first_last=True,
):
    start_time = time.time()  # Start timing
    category = category_column

    # Ordena por id e tempo
    df = df.sort_values(by=["id", "t"])

    # Converte para GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.x, df.y), crs="EPSG:4326"
    )
    gdf = gdf.to_crs(epsg=3857)

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

    # Pega categorias únicas e define um mapa de cores
    categorias = sorted(gdf[category].unique())
    cmap = cm.get_cmap(
        "tab10", len(categorias)
    )  # você pode trocar por "Set1", "Paired" etc.

    # Cria um plot agregado antes de todos os outros
    fig, ax = plt.subplots()
    if highlight_first_last:
        highlight_first_last_points(ax, gdf)
    for _, traj in gdf.groupby("id"):
        ax.plot(
            traj.geometry.x,
            traj.geometry.y,
            color=cmap(categorias.index(traj[category].iloc[0])),
            linewidth=0.5,
            alpha=0.7,
        )
    ax.set_title(f"{category}", fontsize=16)
    ax.axis("off")
    # Define no plot
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ctx.add_basemap(
        ax,
        source=ctx.providers.Esri.WorldImagery,
        attribution_size=2,
    )
    # Verifica se a pasta de saída existe, se não, cria
    output_path = f"assets/{output_folder}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # Salva o arquivo
    plt.savefig(
        f"assets/{output_folder}/{category}.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)

    for idx, cat in enumerate(categorias):
        sub = gdf[gdf[category] == cat]

        fig, ax = plt.subplots()
        # Destaque os primeiros e últimos pontos das trajetórias
        if highlight_first_last:
            highlight_first_last_points(ax, sub)
        # Agrupa por trajeto (id) e desenha linhas
        for _, traj in sub.groupby("id"):
            ax.plot(
                traj.geometry.x,
                traj.geometry.y,
                color=cmap(idx),
                linewidth=0.5,
                alpha=0.7,
            )

        ax.set_title(f"{category} - {cat}", fontsize=16)
        ax.axis("off")
        # Define no plot
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ctx.add_basemap(
            ax,
            source=ctx.providers.Esri.WorldImagery,
            attribution_size=2,  # ou outro valor menor que o padrão (que é 10)
        )
        # Verifica se a pasta de saída existe, se não, cria
        output_path = f"assets/{output_folder}"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # Salva o arquivo
        plt.savefig(
            f"assets/{output_folder}/{category}_{cat.replace('/', '_')}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close(fig)

    end_time = time.time()  # End timing

    print(f"Imagens salvas para cada {category_column}.")
    print(f"Tempo total de execução: {end_time - start_time} segundos")
    print(f"Arquivos salvos em assets/{output_folder}/")


def main(df, categories):
    # Exemplo de uso
    for col in categories:
        generate_spatial_plots(
            df,
            category_column=col,
            output_folder="Spatial Projection",
        )


if __name__ == "__main__":
    # Carrega os dados
    df = dd.read_csv("./anglova/enriched_anglova.csv").compute()
    # Exemplo de uso
    main(
        df,
        [
            "Company",
            "Company Type",
            "Platoon",
            "Platoon Type",
            "Vehicle Function",
            "Vehicle Type",
            "Command",
        ],
    )
