import pandas as pd

def loop_through_orbital_radii(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Get unique M-site, A-site, and X-site elements
    elements = {
        'M-site': df[['M-site element', 'M-atom s-orbital radii', 'M-atom p-orbital radii', 'M-atom d-orbital radii']].drop_duplicates(),
        'A-site': df[['A-site element', 'A-atom s-orbital radii', 'A-atom p-orbital radii']].drop_duplicates(),
        'X-site': df[['X-site element', 'X-atom s-orbital radii', 'X-atom p-orbital radii']].drop_duplicates()
    }
    
    # Loop through each site type
    for site_type, data in elements.items():
        print(f"\n{site_type} elements:")
        
        # Loop through each unique element within the site type
        for _, row in data.iterrows():
            element_name = row[f'{site_type[0]}-site element']
            
            # Fetch radii values
            s_radius = row.get(f'{site_type[0]}-atom s-orbital radii', 'N/A')
            p_radius = row.get(f'{site_type[0]}-atom p-orbital radii', 'N/A')
            d_radius = row.get(f'{site_type[0]}-atom d-orbital radii', 'N/A')
            
            # Print the radii values for the element
            print(f"{element_name}: s-orbital radius = {s_radius}, p-orbital radius = {p_radius}, d-orbital radius = {d_radius}")

# Example usage
file_path = 'Data/alloys.csv'  # Replace with your CSV file path
loop_through_orbital_radii(file_path)

