# gis_agent.py
class GISAgent:
    """
    Agent responsible for GIS and spatial queries, like address validation, parcel info retrieval, and spatial analysis.
    """
    def __init__(self):
        # Dummy dataset of valid addresses and their parcel info
        self.parcel_database = {
            "123 Main St": {"parcel_id": "555-123-456", "zone": "Residential"},
            "456 Oak Ave": {"parcel_id": "555-789-000", "zone": "Commercial"}
        }

    def verify_address(self, address):
        """
        Verify if the address is within the city's jurisdiction.
        Returns True/parcel info if valid, or False if invalid.
        """
        if address in self.parcel_database:
            return True
        else:
            return False

    def get_parcel_info(self, address):
        """
        Retrieve parcel information (like parcel ID, zoning) for a given address.
        """
        return self.parcel_database.get(address, {})

    def get_nearby_addresses(self, address, radius=500):
        """
        Retrieve a list of nearby addresses within a given radius (for notification purposes).
        """
        # Dummy implementation: just return other addresses in the database as "nearby"
        neighbors = [addr for addr in self.parcel_database.keys() if addr != address]
        return neighbors
