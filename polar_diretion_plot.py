# import time (unused import removed)
import dask.dataframe as dd
import matplotlib.pyplot as plt
# import geopandas as gpd (unused import removed)
# import contextily as ctx (unused import removed)
import os
import matplotlib.cm as cm
import numpy as np


def plot_polar(df, column, hue=None):
    """
    Plots a polar plot of the given column in the DataFrame.

    Parameters:
    - df: DataFrame containing the data to plot.
    - column: The column to plot.
    - hue: Optional. Column to use for color coding.
    - **kwargs: Additional arguments for the plot.

    Returns:
    - None
    """
    # Create a polar plot
    if hue is not None:
        unique_hues = df[hue].unique()
        num_hues = len(unique_hues)
        c = 3  # Number of columns
        r = (num_hues + c - 1) // c  # Calculate the number of rows needed
        fig, axes = plt.subplots(
            r, c, subplot_kw={"projection": "polar"}, figsize=(5 * c, 5 * r)
        )
        axes = axes.flatten()

        colors = cm.rainbow(
            np.linspace(0, 1, num_hues)
        )  # Generate distinct colors
        for i, (h, ax) in enumerate(zip(unique_hues, axes)):  # 'color' removed as it is unused
            directions = df.loc[df[hue] == h, column].dropna()
            kde = np.histogram(
                directions * (np.pi / 180), bins=np.arange(0, 2 * np.pi + np.pi / 18, np.pi / 18)
            )
            ax.plot(
                np.linspace(0, 2 * np.pi, len(kde[0])),
                kde[0],
                alpha=1,
                label=h,
                # color=color,  # Use the generated color
            )
            ax.set_title(h, fontsize=32)
            ax.set_theta_zero_location("N")
            ax.set_rlabel_position(135)
            ax.set_theta_direction(-1)
            ax.set_axisbelow(True)

        # Hide unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        fig.tight_layout()
    else:
        fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
        directions = df.loc[df[hue] == h, column].dropna()
        kde = np.histogram(directions * (np.pi / 180), bins=36)
        ax.plot(
            np.linspace(0, 2 * np.pi, len(kde[0])),
            kde[0],
            alpha=1,
            label=h,
        )
        ax.set_theta_zero_location("N")
        ax.set_rlabel_position(135)
        ax.set_theta_direction(-1)
        ax.set_axisbelow(True)
    # Verifica se a pasta de saída existe, se não, cria
    output_path = "./assets/Direction"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # Salva o arquivo
    plt.savefig(
        f"{output_path}/{hue}_polar.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.savefig(
        f"{output_path}/{hue}_polar.pdf",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)


if __name__ == "__main__":
    df = dd.read_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv"
    ).compute()
    for h in [
        "Company",
        "Company Type",
        "Platoon",
        "Platoon Type",
        "Vehicle Function",
        "Vehicle Type",
        "Command",
    ]:
        plot_polar(df, "direction", hue=h)
