import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="Distributed Clock Synchronization", page_icon="⏱️", layout="wide")

st.title("⏱️ Distributed Clock Synchronization")
st.caption("Berkeley Algorithm Simulation • Distributed Systems Mini Project")
st.info(
    "Simulate clock offsets across distributed nodes. A coordinator collects the offsets, "
    "calculates an average, and sends each online node a correction. This simulation does "
    "not change your computer's actual system clock."
)

st.sidebar.header("Simulation Settings")
num_nodes = st.sidebar.slider("Number of clock nodes", min_value=3, max_value=7, value=5)
coordinator_index = st.sidebar.selectbox(
    "Coordinator node", options=list(range(1, num_nodes + 1)), index=0,
    format_func=lambda n: f"Node {n}"
)
reference_time = st.sidebar.time_input(
    "Reference display time", value=datetime.strptime("10:00:00", "%H:%M:%S").time()
)
st.sidebar.markdown("---")
st.sidebar.write("Positive offsets mean a clock is ahead; negative offsets mean it is behind.")

st.subheader("1. Configure node clocks")
st.caption("Uncheck a node to simulate it being unavailable. The coordinator must remain online.")
cols = st.columns(min(num_nodes, 4))
offsets, online = [], []
default_offsets = [5, 12, -2, -7, 3, 9, -4]
for i in range(num_nodes):
    with cols[i % len(cols)]:
        offsets.append(st.number_input(
            f"Node {i+1} offset (seconds)", min_value=-300, max_value=300,
            value=default_offsets[i], step=1, key=f"offset_{i}"
        ))
        online.append(st.checkbox(f"Node {i+1} online", value=True, key=f"online_{i}"))

reference_dt = datetime.combine(datetime.today(), reference_time)
node_names = [f"Node {i+1}" for i in range(num_nodes)]

def fmt(dt):
    return dt.strftime("%H:%M:%S")

initial_times = [reference_dt + timedelta(seconds=int(x)) for x in offsets]
before_df = pd.DataFrame({
    "Node": node_names,
    "Role": ["Coordinator" if i + 1 == coordinator_index else "Participant" for i in range(num_nodes)],
    "Status": ["Online" if status else "Offline" for status in online],
    "Initial Offset (sec)": offsets,
    "Initial Clock": [fmt(t) for t in initial_times],
})
st.dataframe(before_df, use_container_width=True, hide_index=True)

if st.button("🔄 Synchronize clocks", type="primary", use_container_width=True):
    if not online[coordinator_index - 1]:
        st.session_state.pop("sync_result", None)
        st.error("The selected coordinator is offline. Bring it online or select another coordinator.")
    else:
        active_indices = [i for i, status in enumerate(online) if status]
        active_offsets = [float(offsets[i]) for i in active_indices]
        average_offset = sum(active_offsets) / len(active_offsets)
        corrections = [None] * num_nodes
        corrected_offsets = [None] * num_nodes
        corrected_times = [None] * num_nodes
        for i in active_indices:
            # Berkeley-style correction: target average offset minus this node's current offset.
            corrections[i] = round(average_offset - float(offsets[i]), 2)
            corrected_offsets[i] = round(float(offsets[i]) + corrections[i], 2)
            corrected_times[i] = reference_dt + timedelta(seconds=corrected_offsets[i])
        st.session_state["sync_result"] = {
            "average_offset": average_offset,
            "corrections": corrections,
            "corrected_offsets": corrected_offsets,
            "corrected_times": corrected_times,
            "offsets": list(offsets),
            "online": list(online),
            "node_names": list(node_names),
            "coordinator_index": coordinator_index,
            "reference_dt": reference_dt,
            "active_count": len(active_indices),
        }

if "sync_result" in st.session_state:
    result = st.session_state["sync_result"]
    st.subheader("2. Synchronization results")
    c1, c2, c3 = st.columns(3)
    c1.metric("Coordinator", f"Node {result['coordinator_index']}")
    c2.metric("Average offset of online nodes", f"{result['average_offset']:.2f} sec")
    c3.metric("Online nodes synchronized", f"{result['active_count']}/{len(result['node_names'])}")

    correction_display = ["Offline" if c is None else f"{c:+.2f}" for c in result["corrections"]]
    final_offset_display = ["—" if x is None else f"{x:.2f}" for x in result["corrected_offsets"]]
    final_time_display = ["Unavailable" if t is None else fmt(t) for t in result["corrected_times"]]
    result_df = pd.DataFrame({
        "Node": result["node_names"],
        "Status": ["Online" if x else "Offline" for x in result["online"]],
        "Initial Offset (sec)": result["offsets"],
        "Correction Applied (sec)": correction_display,
        "Final Offset (sec)": final_offset_display,
        "Final Clock": final_time_display,
    })
    st.dataframe(result_df, use_container_width=True, hide_index=True)

    st.subheader("3. Clock offsets before and after synchronization")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    active_indices = [i for i, status in enumerate(result["online"]) if status]
    width = 0.36
    before_values = [result["offsets"][i] for i in active_indices]
    after_values = [result["corrected_offsets"][i] for i in active_indices]
    positions = list(range(len(active_indices)))
    ax.bar([p - width / 2 for p in positions], before_values, width, label="Before")
    ax.bar([p + width / 2 for p in positions], after_values, width, label="After")
    ax.axhline(0, linewidth=1)
    ax.set_xticks(positions)
    ax.set_xticklabels([result["node_names"][i] for i in active_indices])
    ax.set_ylabel("Offset from reference (seconds)")
    ax.set_title("Clock Offset Comparison (online nodes)")
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    st.success("Synchronization completed. All online simulated nodes now share the calculated average offset.")

    with st.expander("How the Berkeley-style algorithm works"):
        st.markdown(
            """
            1. The coordinator collects clock offsets from online nodes, including itself.
            2. It calculates the average offset of those nodes.
            3. For each online node, it calculates **correction = average offset − current offset**.
            4. Each online node applies its correction; its final offset becomes the average offset.
            5. Offline nodes are excluded from the average and remain unsynchronized in this run.

            **Scope:** This is an educational simulation. A real Berkeley implementation estimates
            times from network messages and may account for communication delays and clock drift.
            """
        )

st.markdown("---")
st.caption("Distributed Systems Mini Project • Clock Synchronization • Berkeley-style algorithm")
