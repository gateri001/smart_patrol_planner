import pandas as pd

def run_bias_check(dataset_path="../datasets/sample_incidents.csv"):
    # Load dataset
    df = pd.read_csv(dataset_path)

    # Group by region (or any relevant column)
    region_counts = df['region'].value_counts(normalize=True) * 100

    print("=== Bias Check Report ===")
    print("Distribution of incidents by region (%):")
    print(region_counts)

    # Simple fairness indicator: flag imbalance if >30% difference
    max_region = region_counts.max()
    min_region = region_counts.min()

    if max_region - min_region > 30:
        print("\n⚠️ Potential imbalance detected: "
              f"Difference between regions = {max_region - min_region:.2f}%")
    else:
        print("\n✅ No major imbalance detected.")

if __name__ == "__main__":
    run_bias_check()

