""" Remember, to use a file in sage, you have to
`attach([file])`. 

The grey algorithm simply cycle to all possible edge
orientations permutations to generate all the possible
orientations.
 """

from time import process_time_ns


def compute_orientations_grey_algorithm(graph):
    a = process_time_ns()
    orientations = grey_algorithm(graph)
    b = process_time_ns()
    print(
        f"Found {orientations} orientations in {(b-a)/1000000000}s"
    )

def grey_algorithm(graph):
    orientations = []
    initial_orientation = graph.edges(labels=False)
    orientations.append(initial_orientation)
    for idx, edge in enumerate(initial_orientation):
        u, v = edge
        prev_orientation = orientations[-1]
        next_orientation = prev_orientation[:idx+1] + [(v,u)] + prev_orientation[idx+2:]
        import pdb
        pdb.set_trace()
        orientations.append(next_orientation)
    return orientations


triangle_orientations = [[(0,1),(1,2),(2,0)]]
class TestGreyAlgorithm:
    """How can you test sage files?"""

    def test_grey_algorithm_triangle(self):
        graph = Graph([(0,1),(1,2),(2,0)])
        orientations = grey_algorithm(graph)
        assert orientations == triangle_orientations
