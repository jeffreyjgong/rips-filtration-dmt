from typing import List, Self

class VRFiltrationIndexedCell:
    """
    A class to represent a n-dimensional cell.

    Attributes:
    - vertices (list): A list of indices representing the vertices of the cell
    - dimension (int): Dimension of the cell
    - facets (list): A list of facets of the cell
    - cofacets (list): A list of cofacets of the cell
    """

    def __init__(self, vertices: List[int]):
        """
        Initialize a new cell with the given vertex indices

        Parameters:
        vertices (list): A list of indices representing the vertices of the cell
        """

        assert(len(vertices) > 0)
        assert(len(set(vertices)) == len(vertices))
        self.vertex_set = set(vertices)
        self.dimension = len(vertices) - 1
        self.facets: List[Self] = []
        self.cofacets: List[Self] = []
    
    def add_facet(self, other: Self):
        """
        Add a facet to the list of facets
        """
        self.facets.append(other)

    def add_cofacet(self, other: Self):
        assert(self.is_facet_of(other))
        self.cofacets.append(other)
    
    def is_facet_of(self, other: Self):
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
    
class VRFiltrationSimplicialComplex:
    """
    A class to represent a VR Filtration simplicial complex

    Attributes:
    - maximal_simplices (list): A list of IndexedCells representing the maximal simplices
    - num_vertices (int): A number of vertices, assumed to be unchanging
    - dimension (int): The dimension of the maximal simplex
    - n_simplex_dict (dict): A dictionary of all the simplices per dimension
    """
    
    def __init__(self, maximal_simplices: List[VRFiltrationIndexedCell]):
        # check that each vertex is represented from [1,n]
        vertex_tracker = set()
        for maximal_simplex in maximal_simplices:
            for vertex_index in maximal_simplex.sorted_vertices:
                vertex_tracker.add(vertex_index)
        
        max_vertex = max(vertex_tracker)
        full_range = set(range(1, max_vertex+1))

        assert(full_range.issubset(vertex_tracker))

        # 

def main():
    bruh = VRFiltrationIndexedCell([1,2,3])
    bruhh = VRFiltrationIndexedCell([3])

    print(bruhh.is_facet_of(bruh))


if __name__ == "__main__":
    main()


    
