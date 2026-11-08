unstable_periods = df[
#     df["Network_Status"] == "Unstable"
# ][
#     ["DateTime", "Machine_ID",
#      "Network_Latency_ms",
#      "Packet_Loss_%",
#      "Efficiency_Status"]
# ]

# print(unstable_periods.head(20))

# df["Timestamp"] = df["DateTime"].dt.floor("h")