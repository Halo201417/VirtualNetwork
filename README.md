# Execution Guide: Transport Protocol Analysis in Mininet

This guide details the exact steps to reproduce the network topology simulating a "Coffee Shop Wi-Fi" environment (4% packet loss, 5ms delay) and to extract the Congestion Window (CWND) metrics for the TCP Reno, BBR, and CUBIC algorithms.

## Prerequisites
Make sure you have the system tools and Python libraries installed:
```bash
sudo apt update && sudo apt install mininet iperf3 tcpdump tshark
pip install pandas matplotlib
```

---

## Phase 1: Start Topology and Verification
1. Start the Mininet network by running the main script (outside the Python virtual environment):
   ```bash
   sudo python3 topology.py
   ```
2. Perform a *Sanity Check* in the `mininet>` console to verify that the 8% total loss (round-trip) is being applied:
   ```text
   mininet> h1 ping -c 50 h2
   ```

*(Important Note: Run `sudo mn -c` in your normal terminal if Mininet crashes at any point to clean up zombie interfaces).*

---

## Phase 2: Congestion Algorithms Measurement

### Test 1: TCP Reno
From the `mininet>` console, run the following sequence:
1. **Configure the algorithm:**
   ```text
   mininet> h1 sysctl -w net.ipv4.tcp_congestion_control=reno
   mininet> h2 sysctl -w net.ipv4.tcp_congestion_control=reno
   ```
2. **Start the server in the background:**
   ```text
   mininet> h2 iperf3 -s &
   ```
3. **Start packet capture in the background:**
   ```text
   mininet> h1 tcpdump -i h1-eth0 -w reno.pcap &
   ```
4. **Inject massive traffic for 20 seconds:**
   ```text
   mininet> h1 iperf3 -c 10.0.2.2 -t 20
   ```
5. **Stop capture and exit:**
   ```text
   mininet> h1 killall tcpdump
   mininet> exit
   ```
*(Run `sudo mn -c` in your normal terminal before the next test).*

### Test 2: TCP BBR
BBR requires the module to be loaded on the host system and the *Fair Queuing* (FQ) discipline to be configured on the Mininet interfaces.
1. **Load the module on the base system (in a normal terminal):**
   ```bash
   sudo modprobe tcp_bbr
   ```
2. **Start the topology again:**
   ```bash
   sudo python3 topology.py
   ```
3. **Apply the FQ queue on the Mininet nodes:**
   ```text
   mininet> h1 tc qdisc replace dev h1-eth0 root fq
   mininet> h2 tc qdisc replace dev h2-eth0 root fq
   ```
4. **Configure the BBR algorithm and run the test:**
   ```text
   mininet> h1 sysctl -w net.ipv4.tcp_congestion_control=bbr
   mininet> h2 sysctl -w net.ipv4.tcp_congestion_control=bbr
   mininet> h2 iperf3 -s &
   mininet> h1 tcpdump -i h1-eth0 -w bbr.pcap &
   mininet> h1 iperf3 -c 10.0.2.2 -t 20
   mininet> h1 killall tcpdump
   mininet> exit
   ```
*(Run `sudo mn -c` in your normal terminal before the next test).*

### Test 3: TCP CUBIC
Start the network again (`sudo python3 topology.py`) and run the sequence for CUBIC:
1. **Configure the algorithm:**
   ```text
   mininet> h1 sysctl -w net.ipv4.tcp_congestion_control=cubic
   mininet> h2 sysctl -w net.ipv4.tcp_congestion_control=cubic
   ```
2. **Run the test and capture:**
   ```text
   mininet> h2 iperf3 -s &
   mininet> h1 tcpdump -i h1-eth0 -w cubic.pcap &
   mininet> h1 iperf3 -c 10.0.2.2 -t 20
   mininet> h1 killall tcpdump
   mininet> exit
   ```
*(Run `sudo mn -c` to perform the final cleanup).*

---

## Phase 3: Data Extraction and Graph Generation

Once you have the three files (`reno.pcap`, `bbr.pcap`, `cubic.pcap`) in your directory, activate your Python virtual environment (if you are using one) and run the analysis script to generate the *Bytes in Flight* (CWND) visualizations:

```bash
# Activate the virtual environment (optional, depending on your setup)
source .venv/bin/activate

# Run the analyzer
python3 analyze_pcap.py
```

Upon completion, the script will have generated the `.csv` files with the raw data extracted by `tshark`, as well as three independent images (`reno_graph.png`, `bbr_graph.png`, `cubic_graph.png`) ready for your report.