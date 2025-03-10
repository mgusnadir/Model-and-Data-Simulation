import random

def monte_carlo_pi(num_samples: int) -> float:
    circle_points = 0  # Marbles inside the circular bowl
    square_points = 0  # Marbles inside the square bowl
    
    for _ in range(num_samples):
        rand_x = random.uniform(-1, 1)  # Random x-coordinate
        rand_y = random.uniform(-1, 1)  # Random y-coordinate
        
        origin_dist = rand_x**2 + rand_y**2  # Distance from origin
        
        if origin_dist <= 1:  # Check if marble falls inside the circular bowl
            circle_points += 1
        
        square_points += 1
    
    # Pi is estimated as 4 times the ratio of marbles in the circular bowl to the total marbles
    return 4 * circle_points / square_points

if __name__ == "__main__":
    num_samples = 1_000_000  # Number of marbles dropped
    estimated_pi = monte_carlo_pi(num_samples)
    print(f"Estimated π: {estimated_pi}")
