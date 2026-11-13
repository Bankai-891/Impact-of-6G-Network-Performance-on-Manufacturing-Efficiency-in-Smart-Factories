from  newtwork_profiling import df,pd

print("--"*25,"Packet Loss and Error Rate Analysis" ,"--"*25)
def analyze_packet_loss_error(df):
    
    # Calculate correlation
    correlation = df[['Packet_Loss_%', 'Error_Rate_%']].corr(method='pearson').iloc[0, 1]

    # Divide packet loss into ranges
    df['Packet_Loss_Range'] = pd.cut(df['Packet_Loss_%'],bins=[-float('inf'), 0.5, 1, 2, float('inf')],labels=['Low', 'Moderate', 'High', 'Very High'])

    # Analyze error rate across packet loss ranges
    result = df.groupby('Packet_Loss_Range',observed=False).agg(Total_Records=('Machine_ID', 'count'),Avg_Packet_Loss=('Packet_Loss_%', 'mean'),Avg_Error_Rate=('Error_Rate_%', 'mean')).round(3)

    # Interpret correlation
    if correlation >= 0.7:
        relationship = 'Strong Positive Correlation'
    elif correlation >= 0.3:
        relationship = 'Moderate Positive Correlation'
    elif correlation > 0:
        relationship = 'Weak Positive Correlation'
    elif correlation <= -0.7:
        relationship = 'Strong Negative Correlation'
    elif correlation <= -0.3:
        relationship = 'Moderate Negative Correlation'
    elif correlation < 0:
        relationship = 'Weak Negative Correlation'
    else:
        relationship = 'No Linear Correlation'

    print("\nPACKET LOSS VS ERROR RATE")
    print("Pearson Correlation:", round(correlation, 3))
    print("Relationship:", relationship)

    print("--"*25,"ERROR RATE ACROSS PACKET LOSS RANGES","--"*25)
    print(result)

    return result, correlation

packet_error_results, packet_error_corr = analyze_packet_loss_error(df)



def analyze_packet_loss_defects(df):
    
    # Calculate packet loss spike threshold
    spike_threshold = df['Packet_Loss_%'].quantile(0.90)

    # Classify normal and spike periods
    df['Packet_Loss_Status'] = df['Packet_Loss_%'].apply(lambda x: 'Spike' if x > spike_threshold else 'Normal')

    # Compare defect rates
    result = df.groupby('Packet_Loss_Status').agg(
        Total_Records=('Machine_ID', 'count'),
        Avg_Packet_Loss=('Packet_Loss_%', 'mean'),
        Avg_Defect_Rate=('Quality_Control_Defect_Rate_%', 'mean'),
        Max_Defect_Rate=('Quality_Control_Defect_Rate_%', 'max'),
        Avg_Error_Rate=('Error_Rate_%', 'mean')
    ).round(3)

    # Calculate defect rate change
    normal_defect = result.loc['Normal', 'Avg_Defect_Rate']
    spike_defect = result.loc['Spike', 'Avg_Defect_Rate']

    defect_change = spike_defect - normal_defect

    percentage_change = ((defect_change / normal_defect) * 100 if normal_defect != 0 else None)

    print("\nPACKET LOSS SPIKE ANALYSIS")
    print("Spike Threshold:", round(spike_threshold, 3), "%")

    print("\nNORMAL VS SPIKE PERIODS")
    print(result)

    print("\nDEFECT RATE IMPACT")
    print("Absolute Change:", round(defect_change, 3), "percentage points")

    if percentage_change is not None:
        print("Percentage Change:", round(percentage_change, 2), "%")

    return result

defect_spike_results = analyze_packet_loss_defects(df)

def identify_reliability_thresholds(df):
    
    # Calculate statistical thresholds
    latency_threshold = df['Network_Latency_ms'].quantile(0.75)
    packet_threshold = df['Packet_Loss_%'].quantile(0.75)

    # Classify communication reliability
    def classify_reliability(row):

        latency = row['Network_Latency_ms']
        packet_loss = row['Packet_Loss_%']

        if latency <= latency_threshold and packet_loss <= packet_threshold:
            return 'High Reliability'

        elif latency > latency_threshold and packet_loss > packet_threshold:
            return 'Low Reliability'

        else:
            return 'Moderate Reliability'

    df['Communication_Reliability'] = df.apply(
        classify_reliability, axis=1
    )

    # Analyze performance by reliability level
    result = df.groupby(
        'Communication_Reliability').agg(
        Total_Records=('Machine_ID', 'count'),
        Avg_Latency=('Network_Latency_ms', 'mean'),
        Avg_Packet_Loss=('Packet_Loss_%', 'mean'),
        Avg_Error_Rate=('Error_Rate_%', 'mean'),
        Avg_Defect_Rate=('Quality_Control_Defect_Rate_%', 'mean'),
        Avg_Production_Speed=('Production_Speed_units_per_hr', 'mean')
    ).round(3)

    print("\nCOMMUNICATION RELIABILITY THRESHOLDS")

    print("Latency Threshold:", round(latency_threshold, 3), "ms")
    print("Packet Loss Threshold:", round(packet_threshold, 3), "%")

    print("\nRELIABILITY PERFORMANCE ANALYSIS")
    print(result)

    return result
print("--"*25,"Communication Reliability Thresholds Analysis" ,"--"*25)

reliability_results = identify_reliability_thresholds(df)