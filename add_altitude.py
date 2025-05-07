import json
import time
import urllib.error
import urllib.parse
import urllib.request
import dask.dataframe as dd

ELEVATION_BASE_URL = "https://api.opentopodata.org/v1/test-dataset"


def elevation(lat, lng):
    # Join the parts of the URL together into one string.
    params = urllib.parse.urlencode(
        {
            "location": f"{lat},{lng}",
        }
    )
    url = f"{ELEVATION_BASE_URL}?{params}"

    current_delay = 0.1  # Set the initial retry delay to 100ms.
    time.sleep(current_delay)

    try:
        # Get the API response.
        response = urllib.request.urlopen(url)
    except urllib.error.URLError:
        pass  # Fall through to the retry loop.
    else:
        # If we didn't get an IOError then parse the result.
        result = json.load(response)

        if result["status"] == "OK":
            return result["results"][0]["elevation"]
        elif result["status"] != "UNKNOWN_ERROR":
            # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
            # ZERO_RESULTS. There is no point retrying these requests.
            raise Exception(result["error_message"])

if __name__ == "__main__":
    enriched_points = dd.read_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv",
    ).compute()
    uav = enriched_points[
        enriched_points["Vehicle Function"] == "UAV Reconnaissance"
    ]
    uav["elevation"] = uav.apply(
        lambda row: elevation(row["y"], row["x"]), axis=1
    )
    uav.to_csv(
        "./anglova_metrics_enriched/uav_enriched_metrics.csv",
        index=False,
    )
