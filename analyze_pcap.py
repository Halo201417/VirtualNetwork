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
    
def plot_single_cwnd(csv_file, algo_name, color, output_image):
    print(f"Generating graph for {algo_name}")
    
    if not os.path.exists(csv_file):
        print(f"File {csv_file} does not exist. Skipping.")
        return
        
    plt.figure(figsize=(12, 6)) 
    
    df = pd.read_csv(csv_file, names=["Time", "Bytes_in_Flight"], on_bad_lines='skip').dropna()
    plt.plot(df["Time"], df["Bytes_in_Flight"], label=f"TCP {algo_name}", color=color, linewidth=1.5)
        
    plt.title(f"CWND: {algo_name} - Coffee Shop Wi-Fi (4% Loss)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Bytes in Flight")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"Graph saved as: {output_image}")
    
if __name__ == "__main__":
    extract_cwnd("reno.pcap", "reno.csv")
    extract_cwnd("bbr.pcap", "bbr.csv")
    extract_cwnd("cubic.pcap", "cubic.csv")
    
    plot_single_cwnd("reno.csv", "Reno", "blue", "reno_graph.png")
    plot_single_cwnd("bbr.csv", "BBR", "red", "bbr_graph.png")
    plot_single_cwnd("cubic.csv", "CUBIC", "green", "cubic_graph.png")