import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from Bio import Phylo
from Bio.Phylo import BaseTree
import numpy as np
from io import StringIO

# Create a sample Newick tree string that matches the structure in your image
# You should replace this with your actual phylogenetic tree data
newick_tree = """
(((((A1:0.1,A2:0.1):0.05,(A3:0.08,A4:0.08):0.07):0.1,
   ((B1:0.1,B2:0.1):0.08,(B3:0.1,B4:0.1):0.08):0.07):0.15,
  (((C1:0.1,C2:0.1):0.05,((C3:0.1,C4:0.1):0.03,(C5:0.1,C6:0.1):0.03):0.02):0.1,
   (((D1:0.1,D2:0.1):0.05,(D3:0.1,D4:0.1):0.05):0.08,
    ((D5:0.1,D6:0.1):0.06,(D7:0.1,D8:0.1):0.06):0.07):0.05):0.12):0.2,
 ((((E1:0.1,E2:0.1):0.08,(E3:0.1,E4:0.1):0.08):0.1,
   ((E5:0.1,E6:0.1):0.09,(E7:0.1,E8:0.1):0.09):0.09):0.15,
  (((F1:0.1,F2:0.1):0.07,((F3:0.1,F4:0.1):0.05,(F5:0.1,F6:0.1):0.05):0.02):0.12,
   (((G1:0.1,G2:0.1):0.08,(G3:0.1,G4:0.1):0.08):0.1,
    ((G5:0.1,G6:0.1):0.09,(G7:0.1,G8:0.1):0.09):0.09):0.07):0.08):0.18);
"""

def calculate_tree_layout(tree):
    """Calculate x,y coordinates for all nodes in the tree"""
    # Get all terminals and calculate their y-positions
    terminals = tree.get_terminals()
    
    # Assign y-coordinates to terminals (evenly spaced)
    for i, terminal in enumerate(terminals):
        terminal.y_coord = float(i)
    
    # Calculate x-coordinates based on distance from root
    for clade in tree.find_clades():
        clade.x_coord = tree.distance(tree.root, clade)
    
    # Calculate y-coordinates for internal nodes (average of children)
    for clade in tree.get_nonterminals(order='postorder'):
        if clade.clades:
            clade.y_coord = np.mean([child.y_coord for child in clade.clades])
    
    # Set root coordinates
    if hasattr(tree.root, 'clades') and tree.root.clades:
        tree.root.y_coord = np.mean([child.y_coord for child in tree.root.clades])
    tree.root.x_coord = 0.0
    
    return tree

def draw_tree_custom(tree, ax, color_groups=None):
    """Custom tree drawing function with full control"""
    
    if color_groups is None:
        color_groups = {}
    
    # Calculate layout
    tree = calculate_tree_layout(tree)
    
    def get_color(clade):
        """Get color for a clade based on its name"""
        if clade.name and color_groups:
            # Try to match by first letter or full name
            for key, color in color_groups.items():
                if clade.name.startswith(key) or clade.name == key:
                    return color
        return 'black'
    
    # Draw all branches
    for clade in tree.find_clades():
        if clade == tree.root:
            continue
            
        # Find parent
        parent = None
        for potential_parent in tree.find_clades():
            if clade in potential_parent.clades:
                parent = potential_parent
                break
        
        if parent is None:
            continue
        
        # Determine color and line width
        if clade.is_terminal():
            color = get_color(clade)
            linewidth = 1.5
        else:
            color = 'black'
            linewidth = 1.0
        
        # Draw horizontal line (branch)
        ax.plot([parent.x_coord, clade.x_coord], 
                [clade.y_coord, clade.y_coord], 
                color=color, linewidth=linewidth, solid_capstyle='round')
        
        # Draw vertical line connecting to parent
        ax.plot([parent.x_coord, parent.x_coord], 
                [parent.y_coord, clade.y_coord], 
                color='black', linewidth=1.0, solid_capstyle='round')
    
    return tree

def create_phylogenetic_tree_figure():
    """Create a publication-ready phylogenetic tree figure"""
    
    # Parse the Newick tree
    tree = Phylo.read(StringIO(newick_tree), "newick")
    
    # Create figure with custom size
    fig, ax = plt.subplots(1, 1, figsize=(8, 12))
    
    # Define color groups for different clades
    color_groups = {
        'A': '#D3D3D3',  # Light gray
        'B': '#90EE90',  # Light green  
        'C': '#FFFF99',  # Light yellow
        'D': '#D3D3D3',  # Light gray
        'E': '#90EE90',  # Light green
        'F': '#FFFF99',  # Light yellow
        'G': '#90EE90',  # Light green
    }
    
    # Draw the tree
    tree = draw_tree_custom(tree, ax, color_groups)
    
    # Get tree dimensions
    terminals = tree.get_terminals()
    max_x = max(clade.x_coord for clade in tree.find_clades())
    max_y = len(terminals) - 1
    
    # Add colored bars on the right side
    bar_width = max_x * 0.03
    bar_start_x = max_x * 1.05
    
    # Group terminals by their colors and create colored bars
    color_regions = {}
    for terminal in terminals:
        color_key = terminal.name[0] if terminal.name else 'unknown'
        color = color_groups.get(color_key, 'black')
        
        if color not in color_regions:
            color_regions[color] = []
        color_regions[color].append(terminal.y_coord)
    
    # Draw colored rectangles
    for color, y_positions in color_regions.items():
        if len(y_positions) > 0 and color != 'black':
            y_min = min(y_positions) - 0.4
            y_max = max(y_positions) + 0.4
            height = y_max - y_min
            
            rect = mpatches.Rectangle((bar_start_x, y_min), bar_width, height,
                                    facecolor=color, edgecolor='none', alpha=0.8)
            ax.add_patch(rect)
    
    # Set axis limits and appearance
    ax.set_xlim(-max_x * 0.02, max_x * 1.15)
    ax.set_ylim(-0.5, max_y + 0.5)
    
    # Remove all spines and ticks
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add scale bar
    scale_length = max_x * 0.1
    scale_y = -0.3
    ax.plot([0, scale_length], [scale_y, scale_y], 'k-', linewidth=2)
    ax.text(scale_length/2, scale_y - 0.15, f'{scale_length:.2f}', 
            ha='center', va='top', fontsize=9, weight='bold')
    
    return fig, ax, tree

def load_and_visualize_tree(tree_file_path, file_format='newick', color_groups=None):
    """
    Load a phylogenetic tree from file and create visualization
    
    Parameters:
    tree_file_path: str - path to your tree file
    file_format: str - format of tree file ('newick', 'nexus', 'phyloxml', etc.)
    color_groups: dict - mapping of taxa prefixes to colors
    """
    
    try:
        # Load tree from file
        tree = Phylo.read(tree_file_path, file_format)
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(10, 12))
        
        # Default colors if none provided
        if color_groups is None:
            color_groups = {
                'A': '#FF9999',  # Light red
                'B': '#99FF99',  # Light green
                'C': '#9999FF',  # Light blue
                'D': '#FFFF99',  # Light yellow
                'E': '#FF99FF',  # Light magenta
                'F': '#99FFFF',  # Light cyan
            }
        
        # Draw the tree
        tree = draw_tree_custom(tree, ax, color_groups)
        
        # Customize appearance
        terminals = tree.get_terminals()
        max_x = max(clade.x_coord for clade in tree.find_clades())
        max_y = len(terminals) - 1
        
        ax.set_xlim(-max_x * 0.02, max_x * 1.1)
        ax.set_ylim(-0.5, max_y + 0.5)
        
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        
        return fig, ax, tree
        
    except Exception as e:
        print(f"Error loading tree file: {e}")
        print("Make sure the file exists and is in the correct format.")
        return None, None, None

# Simple example with basic Phylo.draw (alternative method)
def simple_tree_visualization():
    """Simple tree visualization using basic Phylo.draw"""
    
    tree = Phylo.read(StringIO(newick_tree), "newick")
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Use the basic draw function without problematic parameters
    Phylo.draw(tree, axes=ax, do_show=False)
    
    # Clean up appearance
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    return fig, ax, tree

# Main execution
if __name__ == "__main__":
    try:
        # Create the tree figure using custom drawing
        print("Creating phylogenetic tree...")
        fig, ax, tree = create_phylogenetic_tree_figure()
        
        # Adjust layout
        plt.tight_layout()
        
        # Save in publication formats
        plt.savefig('03_biopython_phylo_tree.png', dpi=300, bbox_inches='tight')
        plt.savefig('03_biopython_phylo_tree.pdf', bbox_inches='tight')
        plt.savefig('03_biopython_phylo_tree.svg', bbox_inches='tight')
        
        print("Tree visualization completed successfully!")
        print("Files saved:")
        print("- biopython_phylo_tree.png (300 DPI)")
        print("- biopython_phylo_tree.pdf")
        print("- biopython_phylo_tree.svg")
        
        # Display tree statistics
        terminals = tree.get_terminals()
        nonterminals = tree.get_nonterminals()
        
        print(f"\nTree Statistics:")
        print(f"- Number of terminals (leaves): {len(terminals)}")
        print(f"- Number of internal nodes: {len(nonterminals)}")
        print(f"- Total tree depth: {max(tree.distance(tree.root, t) for t in terminals):.3f}")
        
        # Show the plot
        plt.show()
        
    except Exception as e:
        print(f"Error creating tree: {e}")
        print("Trying alternative simple visualization...")
        
        # Fallback to simple visualization
        try:
            fig, ax, tree = simple_tree_visualization()
            plt.savefig('simple_phylo_tree.png', dpi=300, bbox_inches='tight')
            plt.show()
            print("Simple tree visualization created successfully!")
            
        except Exception as e2:
            print(f"Both methods failed: {e2}")
            print("Please check your Biopython installation.")

# Additional utility functions
def print_tree_structure(tree):
    """Print the tree structure for debugging"""
    print("Tree structure:")
    for clade in tree.find_clades():
        indent = "  " * tree.distance(tree.root, clade, topology_only=True)
        name = clade.name if clade.name else "Internal"
        branch_length = f":{clade.branch_length:.3f}" if clade.branch_length else ""
        print(f"{indent}{name}{branch_length}")

def export_tree_coordinates(tree, filename='tree_coordinates.csv'):
    """Export tree node coordinates for external use"""
    import csv
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Node_Name', 'X_Coordinate', 'Y_Coordinate', 'Branch_Length', 'Is_Terminal'])
        
        for clade in tree.find_clades():
            name = clade.name if clade.name else 'Internal'
            x_coord = getattr(clade, 'x_coord', 0)
            y_coord = getattr(clade, 'y_coord', 0)
            branch_length = clade.branch_length if clade.branch_length else 0
            is_terminal = clade.is_terminal()
            
            writer.writerow([name, x_coord, y_coord, branch_length, is_terminal])
    
    print(f"Tree coordinates exported to {filename}")

# Usage examples:
"""
# To use your own tree file:
fig, ax, tree = load_and_visualize_tree('your_tree.nwk', 'newick')

# To customize colors:
my_colors = {
    'Species': '#FF0000',
    'Genus': '#00FF00', 
    'Family': '#0000FF'
}
fig, ax, tree = load_and_visualize_tree('tree.nwk', color_groups=my_colors)

# To debug tree structure:
print_tree_structure(tree)
"""