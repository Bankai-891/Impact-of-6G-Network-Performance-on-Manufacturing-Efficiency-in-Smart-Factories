from main import df
import pandas as pd
    
print("--"*25,"Network Peformance profiling" ,"--"*25)


# correlation = df["Network_Latency_ms"].corr(
#     df["Packet_Loss_%"]
# )

# print("Correlation:", correlation)

network_analysis = df.groupby("Operation_Mode").agg(
    Avg_Latency=("Network_Latency_ms", "mean"),
    Median_Latency=("Network_Latency_ms", "median"),
    Avg_Packet_Loss=("Packet_Loss_%", "mean"),
    Median_Packet_Loss=("Packet_Loss_%", "median")
)

print(network_analysis)

latency_threshold = df["Network_Latency_ms"].quantile(0.75)
packet_loss_threshold = df["Packet_Loss_%"].quantile(0.75)
print("--"*25,"## Thresholds ##","--"*25)
print("Latency threshold:", latency_threshold)
print("Packet loss threshold:", packet_loss_threshold)

df["Network_Status"] = "Stable"

unstable = ((df["Network_Latency_ms"] > latency_threshold) | (df["Packet_Loss_%"] > packet_loss_threshold))
df.loc[unstable, "Network_Status"] = "Unstable"
print(df["Network_Status"].value_counts())

# network quality 
print("--"*25,"Network Quality check" ,"--"*25)



# Get existing network metrics
latency = df["Network_Latency_ms"]
packet_loss = df["Packet_Loss_%"]

# Normalize the values
def normalize(series):
    value_range = series.max() - series.min()
    if value_range == 0:
        return series * 0
    return (series - series.min()) / value_range

# Calculate network quality score (temporary only)
quality_score = (
    (1 - normalize(latency)) * 0.5
    + (1 - normalize(packet_loss)) * 0.5
)

# Segment network quality without modifying data
network_quality = pd.cut(
    quality_score,
    bins=[-0.001, 0.33, 0.66, 1.001],
    labels=["Low", "Medium", "High"]
)

# Display the results
print("Network Quality Analysis")
print("------------------------")
print(network_quality.value_counts().reindex(
    ["Low", "Medium", "High"], fill_value=0
))

print("\nNetwork Quality Percentage:")
print(
    (network_quality.value_counts(normalize=True) * 100)
    .reindex(["Low", "Medium", "High"], fill_value=0)
    .round(2)
    .astype(str) + "%"
)


# Network vs Efficiency Analysis

# Compare Efficiency_Status across network quality bands


# Define network quality bands
def network_quality(row):
    if row['Network_Latency_ms'] <= 5 and row['Packet_Loss_%'] <= 0.5:
        return 'High'
    elif row['Network_Latency_ms'] <= 15 and row['Packet_Loss_%'] <= 2:
        return 'Medium'
    else:
        return 'Low'

# Apply classification
df['Network_Quality'] = df.apply(network_quality, axis=1)

print("--"*25,"Network Quality Classification" ,"--"*25)
# # Compare efficiency status across network quality
efficiency_comparison = pd.crosstab(df['Network_Quality'],df['Efficiency_Status'] , margins=True, margins_name="Total")
print(efficiency_comparison)



def analyze_latency_efficiency(df):
    
    # Group network latency into ranges
    df['Latency_Range'] = pd.cut(
        df['Network_Latency_ms'],
        bins=[0, 5, 10, 15, 20, float('inf')],
        labels=['0-5 ms', '5-10 ms', '10-15 ms',
                '15-20 ms', 'Above 20 ms']
    )

    # Analyze efficiency metrics
    result = df.groupby(
        'Latency_Range',
        observed=False
    ).agg(
        Total_Records=('Machine_ID', 'count'),
        Avg_Production_Speed=('Production_Speed_units_per_hr', 'mean'),
        Avg_Error_Rate=('Error_Rate_%', 'mean'),
        Avg_Defect_Rate=('Quality_Control_Defect_Rate_%', 'mean')
    ).round(2)

    print("\nLATENCY VS MANUFACTURING EFFICIENCY")
    print(result)

    # Efficiency status percentage
    if 'Efficiency_Status' in df.columns:

        efficiency_status = pd.crosstab(
            df['Latency_Range'],
            df['Efficiency_Status'],
            normalize='index'
        ).mul(100).round(2)

        print("\nEFFICIENCY STATUS DISTRIBUTION (%)")
        print(efficiency_status)

    return result
latency_analysis = analyze_latency_efficiency(df)


print("--"*25,"Network Sensitivity Analysis" ,"--"*25)
def identify_sensitivity_zones(data):
    
    # Divide latency into ranges
    data['Latency_Range'] = pd.cut(
        data['Network_Latency_ms'],
        bins=[0, 5, 10, 15, 20, float('inf')],
        labels=['0-5 ms', '5-10 ms', '10-15 ms',
                '15-20 ms', 'Above 20 ms'],
        include_lowest=True
    )

    # Calculate performance metrics
    analysis = data.groupby(
        'Latency_Range',
        observed=False
    ).agg(
        Avg_Production_Speed=('Production_Speed_units_per_hr', 'mean'),
        Avg_Error_Rate=('Error_Rate_%', 'mean'),
        Avg_Defect_Rate=('Quality_Control_Defect_Rate_%', 'mean')
    ).round(2)

    # Calculate percentage change in production speed
    analysis['Speed_Change_%'] = (
        analysis['Avg_Production_Speed'].pct_change() * 100
    ).round(2)

    # Identify sensitivity zones
    analysis['Performance_Zone'] = analysis['Speed_Change_%'].apply(
        lambda x: (
            'High Sensitivity' if x <= -10
            else 'Moderate Sensitivity' if x <= -5
            else 'Low Sensitivity'
        ) if pd.notna(x) else 'Baseline'
    )

    print("\nNETWORK LATENCY PERFORMANCE SENSITIVITY")
    print(analysis)

    return analysis
sensitivity_results = identify_sensitivity_zones(df)



def production_latency_analysis(df):
    
    result = df.groupby(
        'Latency_Range',
        observed=False
    ).agg(
        Avg_Latency=('Network_Latency_ms', 'mean'),
        Avg_Production_Speed=('Production_Speed_units_per_hr', 'mean'),
        Total_Records=('Machine_ID', 'count')
    ).round(2)

    print("\nPRODUCTION SPEED VS LATENCY")
    print(result)

    return result

production_results = production_latency_analysis(df)
print(production_results)