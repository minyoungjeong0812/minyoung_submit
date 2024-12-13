import json
import networkx as nx
import matplotlib.pyplot as plt

# Assume 'output.json' is the file produced by extract_threat_intel
with open("output.json", "r") as f:
    data = json.load(f)

def visualize_entities_and_relationships(data, output_image='graph.png'):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes with attributes
    for entity in data["entities"]:
        # Use entity 'id' as node key, and store 'name' and 'type' as attributes
        G.add_node(entity["id"], label=entity["name"], etype=entity["type"])

    # Add edges with relationship type as an attribute
    for rel in data["relationships"]:
        G.add_edge(rel["source"], rel["target"], rtype=rel["type"])

    # Generate positions for nodes (you can try different layouts)
    pos = nx.spring_layout(G, seed=42)  # deterministic layout

    # Draw nodes
    node_labels = {node: G.nodes[node]['label'] for node in G.nodes()}
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1500)

    # Draw edges
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15)

    # Draw labels (for nodes and optionally for edges)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9, font_color='black')

    # If you want edge labels (relationship types), uncomment below:
    edge_labels = nx.get_edge_attributes(G, 'rtype')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=10)

    # Remove axis for cleaner look
    plt.axis('off')

    # Save to a file
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Graph saved to {output_image}")

visualize_entities_and_relationships(data, output_image="output_graph.png")