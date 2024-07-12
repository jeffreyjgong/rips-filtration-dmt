from types import NotImplementedType
from typing import Dict, List, Self

class VRFiltrationIndexedCell:
    """
    A class to represent a n-dimensional cell.

    Attributes:
    - vertices (list): A list of indices representing the vertices of the cell
    - dimension (int): Dimension of the cell
    - facets (list): A list of facets of the cell
    - cofacets (list): A list of cofacets of the cell
    """

    def __init__(self, vertices: List[int]) -> None:
        """
        Initialize a new cell with the given vertex indices

        Parameters:
        vertices (list): A list of indices representing the vertices of the cell
        """
        assert(len(vertices) > 0)
        assert(len(set(vertices)) == len(vertices))
        self.vertex_set = set(vertices)
        self.dimension = len(vertices) - 1
        self.co_1_faces: List[Self] = []
        self.co_neg_1_cofaces: List[Self] = []
    
    def add_co_1_face(self, other: Self) -> None:
        """
        Add a codimension 1 face
        """
        assert(other.is_face_of(self) == 1)
        self.co_1_faces.append(other)

    def add_co_neg_1_coface(self, other: Self) -> None:
        """
        Add a codimension -1 face
        """
        assert(self.is_face_of(other) == 1)
        self.co_neg_1_cofaces.append(other)
    
    def is_face_of(self, other: Self) -> int:
        """
        Returns the codimension of other w.r.t self, returns -1 if not a face
        """

        if self.dimension >= other.dimension:
            return -1
        
        if self.vertex_set.issubset(other.vertex_set):
            return len(other.vertex_set) - len(self.vertex_set)
        
        return -1

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, VRFiltrationIndexedCell):
            return NotImplemented
        
        return self.vertex_set == other.vertex_set

    def __repr__(self) -> str:
        return f"{list(self.vertex_set)}"
    
class VRFiltrationSimplicialComplex:
    """
    A class to represent a VR Filtration simplicial complex

    Attributes:
    - maximal_simplices (list): A list of IndexedCells representing the maximal simplices
    - num_vertices (int): A number of vertices, assumed to be unchanging
    - dimension (int): The dimension of the maximal simplex
    - n_cell_dict (dict): A dictionary of all the simplices per dimension
    """
    
    def __init__(self, maximal_simplices: List[VRFiltrationIndexedCell], check_initial_connect: bool = True) -> None:
        self._check_no_faces(maximal_simplices)
        self.num_vertices = self._check_and_output_full_vertex_range(maximal_simplices)
        if check_initial_connect:
            assert(self.sc_ensure_all_connected(maximal_simplices))
        
        self.dimension = max((len(cell_iter.vertex_set) - 1) for cell_iter in maximal_simplices)
        self.n_cell_dict: Dict[int, List[VRFiltrationIndexedCell]] = {}
        
        for dim in range(0, self.dimension+1):
            self.n_cell_dict[dim] = []
        
        for maximal_simplex in maximal_simplices:
            self._enumerate_and_add(maximal_simplex)

    @classmethod
    def from_ints(cls, maximal_simplices_as_vertices: List[List[int]], check_initial_connect: bool = True) -> None:
        return cls([VRFiltrationIndexedCell(lst) for lst in maximal_simplices_as_vertices], check_initial_connect)
    
    def _check_and_output_full_vertex_range(self, maximal_simplices: List[VRFiltrationIndexedCell]) -> int:
        # check that each vertex is represented from [1,n]
        vertex_tracker = set()
        for maximal_simplex in maximal_simplices:
            for vertex_index in maximal_simplex.vertex_set:
                vertex_tracker.add(vertex_index)
        
        max_vertex = max(vertex_tracker)
        full_range = set(range(1, max_vertex+1))

        assert(full_range.issubset(vertex_tracker))
        
        return max_vertex
    
    def _check_no_faces(self, maximal_simplices: List[VRFiltrationIndexedCell]) -> None:
        # check that no maximal simplices are faces of each other
        for i in range(len(maximal_simplices)-1):
            for j in range(i+1, len(maximal_simplices)):
                assert(maximal_simplices[i].is_face_of(maximal_simplices[j]) == -1)
                assert(maximal_simplices[j].is_face_of(maximal_simplices[i]) == -1)
    
    def sc_ensure_all_connected(self, components: List[VRFiltrationIndexedCell]) -> bool:
        if not components:
            return True

        # Flatten the list of components and find the maximum element to determine the size of UnionFind
        flat_list = [item for component in components for item in component.vertex_set]
        max_element = max(flat_list)
        
        # Initialize UnionFind
        uf = UnionFind(max_element + 1)  # +1 because elements are 1-indexed

        # Union all elements within each component
        for component in components:
            component_vertex_lst = list(component.vertex_set)
            for i in range(1, len(component_vertex_lst)):
                uf.union(component_vertex_lst[i - 1], component_vertex_lst[i])

        # Find the root of the first element
        first_root = uf.find(flat_list[0])

        # Check if all elements have the same root
        for element in flat_list:
            if uf.find(element) != first_root:
                return False

        return True
    
    def add_maximal_simplex(self, maximal_simplex: VRFiltrationIndexedCell) -> None:
        # check if already in the dictionary
        pass
    
    def _add_cell(self, cell_to_add: VRFiltrationIndexedCell) -> None:
        """
        Function to add a cell to the cell dict

        Assumes
        - dimension has already been set
        """
        assert(cell_to_add.dimension >= 0 and cell_to_add.dimension <= self.dimension)
        if cell_to_add not in self.n_cell_dict[cell_to_add.dimension]:
            self.n_cell_dict[cell_to_add.dimension].append(cell_to_add)
    
    def _enumerate_and_add(self, maximal_simplex: VRFiltrationIndexedCell) -> None:
        dim = maximal_simplex.dimension
        max_enum = (1 << (dim + 1)) - 1
        vtx_lst = list(maximal_simplex.vertex_set)

        for enum_iter in range(1, max_enum+1):
            indices_to_add = self._binary_format_list(enum_iter, dim+1)
            cell_face_lst = []
            for index_to_add, bin_val in enumerate(indices_to_add):
                if bin_val == 1:
                    cell_face_lst.append(vtx_lst[index_to_add])
            
            self._add_cell(VRFiltrationIndexedCell(cell_face_lst))

    
    def _binary_format_list(self, num: int, size: int) -> List[int]:
        binary_representation = bin(num)[2:][::-1]

        binary_list = [int(bit) for bit in binary_representation]

        # ensure list is of specified size by padding w zeros
        while len(binary_list) < size:
            binary_list.append(0)
        
        return binary_list[:size]
    

    def __repr__(self) -> str:
        repr_str = ""
        for dim in range(0, self.dimension+1):
            repr_str += f"{dim} ({len(self.n_cell_dict[dim])}) - {self.n_cell_dict[dim]}"
            repr_str += "\n\n"
        
        return repr_str

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])  # Path compression
        return self.parent[p]

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)

        if rootP != rootQ:
            # Union by rank
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1


def main():
    bruh = VRFiltrationIndexedCell([1,2,3])
    bruhh = VRFiltrationIndexedCell([3])
    cell_1 = VRFiltrationIndexedCell([5,6])
    cell_2 = VRFiltrationIndexedCell([4,5,6])

    print(bruhh.is_face_of(bruh))

    # check no faces
    # bruhhh = VRFiltrationSimplicialComplex([bruh, bruhh])

    # check full range
    # sc_1 = VRFiltrationSimplicialComplex([cell_1, bruh])

    # check fully connected and optionality
    # sc_2 = VRFiltrationSimplicialComplex([cell_2, bruh], False)

    # check bin format list
    # print(_binary_format_list(31, 5))
    # hello_world = VRFiltrationSimplicialComplex.from_ints([[1,2,3], [3,4], [4,5,6,7]])


    # print(hello_world)

    hello_world_2 = VRFiltrationSimplicialComplex.from_ints([[1,2,3,4,5,6]])
    hello_world_3 = VRFiltrationSimplicialComplex.from_ints([[1,2,3], [3,4,5]])
    print(hello_world_3)
    print("yay it's the triangle numbers so its right")



if __name__ == "__main__":
    main()


    
