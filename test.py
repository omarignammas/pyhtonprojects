import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time

def kruskal_mst_animation(edges):
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    # Initialize an empty graph
    G = nx.Graph()
    
    # Add routers (nodes) from edges
    for u, v, bandwidth in edges:
        G.add_edge(u, v, bandwidth=bandwidth)
    
    # Compute Minimum Spanning Tree (MST) using Kruskal's algorithm step by step
    mst = nx.Graph()
    mst_edges = []
    sorted_edges = edges.copy()
    sorted_edges.sort(key=lambda x: x[2])  # Sort edges by weight
    
    # Initialize Union-Find data structure
    parent = {node: node for node in G.nodes}
    
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]
    
    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            parent[root2] = root1
    
    # Animation: Build MST step by step
    for u, v, bandwidth in sorted_edges:
        if find(u) != find(v):  # Check if u and v are not already in the same set (avoid cycle)
            union(u, v)
            mst.add_edge(u, v, bandwidth=bandwidth)
            mst_edges.append((u, v))
            
            # Display current state of the graph
            plt.clf()
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=12, font_color='black')
            
            # Highlight MST edges
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2.0)
            
            # Display edge labels (bandwidth) on MST edges
            edge_labels = {(u, v): f"{d['bandwidth']} " for (u, v, d) in mst.edges(data=True)}
            nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels, ax=plt.gca())
            
            st.pyplot(plt)
            time.sleep(0.5)  
    
    return mst

def main():
    st.title("Minimum Spanning Tree (MST) Visualization")
    
    # Input number of routers (nodes)
    num_routers = st.number_input("Enter number of switchs:", min_value=1, step=1, value=1)
    
    # Input edges (connections between routers)
    st.subheader("Enter connections (u, v, weight) one by one:")
    edges = []
    
    for i in range(num_routers - 1):
        u = st.text_input(f"Enter router u for connection {i+1}:")
        v = st.text_input(f"Enter router v for connection {i+1}:")
        bandwidth = st.number_input(f"Enter weight for connection {i+1}:", min_value=0, step=1)
        edges.append((u, v, bandwidth))
    
    if st.button("Submit Connections"):
        if not edges:
            st.warning("No valid connections submitted.")
            return
        
        # Generate MST using Kruskal's algorithm with animation
        mst = kruskal_mst_animation(edges)
        
        # Display final MST
        st.subheader("Minimum Spanning Tree Network :")
        fig, ax = plt.subplots()
        pos = nx.spring_layout(mst)  # Compute layout for better visualization
        nx.draw(mst, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=12, font_color='black', ax=ax)
        
        # Add edge labels (bandwidth) to the graph
        edge_labels = {(u, v): f"{d['bandwidth']} " for (u, v, d) in mst.edges(data=True)}
        nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels, ax=ax)
        
        st.pyplot(fig)

if __name__ == "__main__":
    main()
