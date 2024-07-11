class IndexedCell:
    """
    A class to represent a n-dimensional cell.

    Attributes:
    - vertices (list): A list of indices representing the vertices of the cell
    - dimension (int): Dimension of the cell
    - faces (list): A list of faces of the cell
    """
    def __init__(self, vertices):
        """
        Initialize a new cell with the given vertex indices

        Parameters:
        vertices (list): A list of indices representing the vertices of the cell
        """

        assert(len(vertices) > 0)
        assert(len(set(vertices)) == len(vertices))
        self.sorted_vertices = sorted(vertices)
        self.dimension = len(vertices) - 1
        self.facets = []
        self.cofacets = []
    
    def add_facet(self, other):
        """
        Add a facet to the list of facets
        """
        self.facets.append(other)

    def add_cofacet(self, other):
        assert(self.is_facet_of(other))
        self.cofacets.append(other)
    
    def is_facet_of(self, other):
        # assumes sorted
        if self.dimension != other.dimension - 1:
            return False

        found_mismatch = False

        for i in range(self.dimension + 1):
            if found_mismatch:
                if self.sorted_vertices[i] != other.sorted_vertices[i+1]:
                    return False 
            else:
                if self.sorted_vertices[i] != other.sorted_vertices[i]:
                    found_mismatch = True 
        
        return True

    def __repr__(self):
        return f"{self.dimension}-Cell: {self.sorted_vertices}"
    

def main():
    bruh = IndexedCell([1,2,3])
    bruhh = IndexedCell([3])

    print(bruhh.is_facet_of(bruh))


if __name__ == "__main__":
    main()


    
