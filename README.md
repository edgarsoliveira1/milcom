# MILCOM2025 Anglova Tactical Mobility Scenario Analysis

This repository contains the code used for the characterization and analysis of a tactical mobility scenario, as presented in the paper submitted to MILCOM 2025. The study leverages the Anglova scenario, a military mobility benchmark, to extract metrics, perform statistical analyses, and generate detailed visualizations of vehicle movement, connectivity, and leadership patterns in tactical operations.

## Description

The repository includes scripts and notebooks for:
- Enriching trajectory data with mobility metrics (distance, speed, acceleration, tortuosity, etc.).
- Analyzing vehicle connectivity (pairwise distances, proximity time, connected components).
- Identifying leadership and following patterns among units.
- Generating statistical plots (KDE, ECDF, histograms) and spatial/spatiotemporal maps.
- Visualizing coverage, density, and distribution of vehicles by different categories (company, platoon, role, type, command).

## Data Structure

The data used is derived from the Anglova scenario, processed and enriched in:
- `./anglova_metrics_enriched/points_enriched_metrics.csv`: per-point trajectory metrics.
- `./anglova_metrics_enriched/trajectories_enriched_metrics.csv`: aggregated trajectory metrics.

## Main Scripts and Notebooks

- `main_pipeline.py`: main pipeline for processing and metric generation.
- `add_altitude.py`, `add_destine_arrive_time.py`, `add_map_matching.py`: data enrichment scripts.
- `plot_mean_speed_over_time.py`, `plot_convex_hull.py`, `plot_path_tortuosity.ipynb`, `plot_total_distances.ipynb`, `plot_density_over_time.ipynb`, `plot_spatiotemporal_coverage.ipynb`: plotting and mapping.
- `connected_unites_over_time.py`, `connectivity.ipynb`, `plot_connectivity.ipynb`: connectivity analysis.
- `leader.ipynb`, `leader_following_patterns.ipynb`: leadership and following pattern analysis.
- `moveminer/`: main module with calculation strategies, utilities, and visualization.

## How to Reproduce

1. **Prerequisites**  
   - Python 3.10+  
   - Install dependencies:
     ```sh
     pip install -r requirements.txt
     ```

2. **Organize the data**  
   - Place the Anglova CSV files in the `./anglova_metrics_enriched/` folder.

3. **Run the pipeline**  
   - To process and generate metrics:
     ```sh
     python main_pipeline.py
     ```
   - For specific analyses, run the desired notebooks or scripts.

4. **Results**  
   - Generated plots and maps will be saved in the [`assets`](assets) folder or corresponding subfolders.

## Reference

If you use this code, please cite the corresponding paper submitted to MILCOM 2025.

---

**Contact:**  
For questions or collaborations, please contact the