"""Simple closest-pair algorithms.

Each point is stored as (x, y, original_index).
Keeping the original index lets the answer refer to the input list.
"""

from math import sqrt


def squared_distance(first, second):
    """Return the squared distance between two indexed points."""
    # Find the horizontal difference.
    dx = first[0] - second[0]
    # Find the vertical difference.
    dy = first[1] - second[1]
    # Do not use sqrt here because squared distances are enough for comparison.
    return dx * dx + dy * dy


def better_pair(first, second):
    """Return the pair with the smaller squared distance."""
    # A missing pair means that the first pair automatically wins.
    if second is None:
        return first
    # Keep the first pair when it is smaller or tied.
    if first[0] < second[0]:
        return first
    return second


def brute_indexed(points):
    """Check every pair in an indexed list."""
    # No pair has been found yet.
    best = None
    # Choose the first point of a pair.
    for first_position in range(len(points)):
        # Choose a later point so each pair is checked once.
        for second_position in range(first_position + 1, len(points)):
            first = points[first_position]
            second = points[second_position]
            # Store distance and indices in sorted index order.
            candidate = (
                squared_distance(first, second),
                min(first[2], second[2]),
                max(first[2], second[2]),
            )
            # Keep the closest pair seen so far.
            best = better_pair(candidate, best)
    return best


def closest_pair_brute(points):
    """Return (distance, i, j) by checking every pair."""
    # Add each point's original position.
    indexed = [(point[0], point[1], index) for index, point in enumerate(points)]
    # Reject invalid input clearly.
    if len(indexed) < 2:
        raise ValueError("at least two points are required")
    # Find the best squared distance.
    best = brute_indexed(indexed)
    # Take the square root only once, at the end.
    return sqrt(best[0]), best[1], best[2]


def solve_recursive(points_by_x):
    """Return best squared pair and the same points sorted by y."""
    # Small groups are easiest to solve directly.
    if len(points_by_x) <= 3:
        best = brute_indexed(points_by_x)
        by_y = sorted(points_by_x, key=lambda point: (point[1], point[0], point[2]))
        return best[0], best[1], best[2], by_y

    # Split the x-sorted list into two halves.
    middle = len(points_by_x) // 2
    left = points_by_x[:middle]
    right = points_by_x[middle:]
    # The first point in the right half gives the dividing x-coordinate.
    dividing_x = right[0][0]

    # Solve both halves recursively.
    left_best = solve_recursive(left)
    right_best = solve_recursive(right)
    # Start with the better pair from the two halves.
    best = better_pair(left_best[:3], right_best[:3])
    delta_squared = best[0]

    # Merge the two y-sorted lists in linear time.
    left_y = left_best[3]
    right_y = right_best[3]
    by_y = []
    left_position = 0
    right_position = 0
    while left_position < len(left_y) and right_position < len(right_y):
        left_key = (left_y[left_position][1], left_y[left_position][0], left_y[left_position][2])
        right_key = (right_y[right_position][1], right_y[right_position][0], right_y[right_position][2])
        if left_key <= right_key:
            by_y.append(left_y[left_position])
            left_position += 1
        else:
            by_y.append(right_y[right_position])
            right_position += 1
    # Copy any remaining points from either list.
    by_y.extend(left_y[left_position:])
    by_y.extend(right_y[right_position:])

    # Keep points within delta of the dividing line.
    strip = [
        point
        for point in by_y
        if (point[0] - dividing_x) ** 2 <= delta_squared
    ]

    # Check nearby points in y-order.
    for first_position in range(len(strip)):
        # Geometry proves that only a constant number of neighbours are needed.
        end = min(first_position + 8, len(strip))
        for second_position in range(first_position + 1, end):
            first = strip[first_position]
            second = strip[second_position]
            # Later points are too far vertically once this condition is true.
            if (second[1] - first[1]) ** 2 > delta_squared:
                break
            # Compare this possible pair with the current answer.
            candidate = (
                squared_distance(first, second),
                min(first[2], second[2]),
                max(first[2], second[2]),
            )
            best = better_pair(candidate, best)
            # A smaller distance makes the strip condition stricter.
            delta_squared = best[0]

    # Return the answer and the y-sorted list for the parent call.
    return best[0], best[1], best[2], by_y


def closest_pair(points):
    """Return (distance, i, j) using divide and conquer."""
    # Reject invalid input clearly.
    if len(points) < 2:
        raise ValueError("at least two points are required")
    # Attach each point's original index.
    indexed = [(point[0], point[1], index) for index, point in enumerate(points)]
    # Perform the one initial x-sort.
    points_by_x = sorted(indexed, key=lambda point: (point[0], point[1], point[2]))
    # Recursion uses squared distances until this final square root.
    best = solve_recursive(points_by_x)
    return sqrt(best[0]), best[1], best[2]