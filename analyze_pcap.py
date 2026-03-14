import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import os

def extract_cwnd(pcap_file, csv_file):
    print(f"Extracting data from {pcap_file}")
    
    cmd = [
        "tshark", "-r", pcap_file,
        "-Y", "tcp.analysis.bytes_in_flight",
        "-T", "fields",
        "-e", "frame.time_relative",
        "-e", "tcp.analysis.bytes_in_flight",
        "-E", "separator=,"
    ]
    
    with open(csv_file, "w") as outfile:
        subprocess.run(cmd, stdout=outfile)
    
    print("Data extracted in a csv")
    
def plot_cwnd(csv_file, output_image):
    print("Generating graph of congestion")
    
    df = pd.read_csv(csv_file, names=["Time", "Bytes_in_Flight"], on_bad_lines='skip')
    df = df.dropna()
    
    plt.figure(figsize=(12,6))
    plt.plot(df["Time"], df["Bytes_in_Flight"], label="TCP Reno", color='blue', linewidth=1)
    
    plt.title("CWND - Reno")
    plt.xlabel("Time (Seconds)")
    plt.ylabel("Bytes in Flight")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.savefig(output_image, dpi=300)
    print(f"Graph saved as: {output_image}")
    
if __name__ == "__main__":
    pcap_name = "reno.pcap"
    csv_name = "reno.csv"
    img_name = "reno_graph.png"
    
    if os.path.exists(pcap_name):
        extract_cwnd(pcap_name, csv_name)
        plot_cwnd(csv_name, img_name)
    else:
        print(f"Error: File not found")