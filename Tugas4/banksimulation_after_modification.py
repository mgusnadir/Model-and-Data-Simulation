import random
import numpy as np
import matplotlib.pyplot as plt
import simpy

# Simulation Parameters
RANDOM_SEED = 42
NUM_TELLERS = 3      # Number of bank tellers
ARRIVAL_RATE = 5      # Average arrival rate (customers per minute)
SERVICE_RATE = 7      # Average service rate (customers served per minute)
SIM_TIME = 20        # Total simulation time in minutes
VIP_PROBABILITY = 0.2 # Probability of a customer being VIP

# Store waiting times and teller utilization
wait_times = []
teller_busy_time = [0] * NUM_TELLERS

class BankQueueSimulation:
    def __init__(self, env, num_tellers, service_rate):
        self.env = env
        self.teller = simpy.PriorityResource(env, num_tellers)  # Priority queue for VIP customers
        self.service_rate = service_rate
        self.teller_usage = [0] * num_tellers  # Track teller busy times

    def serve_customer(self, customer_id, teller_id):
        """Simulate service process for a customer"""
        service_time = random.expovariate(self.service_rate)
        self.teller_usage[teller_id] += service_time  # Track utilization
        yield self.env.timeout(service_time)
        print(f"Customer {customer_id} finished service at {self.env.now:.2f} min.")

def customer_process(env, customer_id, bank, is_vip):
    """Simulates a customer entering the queue"""
    arrival_time = env.now
    print(f"Customer {customer_id} ({'VIP' if is_vip else 'Regular'}) arrives at {arrival_time:.2f} min.")

    with bank.teller.request(priority=0 if is_vip else 1) as request:
        yield request  # Wait for an available teller
        wait_time = env.now - arrival_time  # Compute waiting time
        wait_times.append(wait_time)

        print(f"Customer {customer_id} starts service after waiting {wait_time:.2f} min.")
        teller_id = random.randint(0, NUM_TELLERS - 1)  # Assign random teller
        yield env.process(bank.serve_customer(customer_id, teller_id))

def customer_arrivals(env, bank, arrival_rate):
    """Generate customers at random arrival intervals"""
    customer_id = 0
    while True:
        yield env.timeout(random.expovariate(arrival_rate))  # Time until next arrival
        customer_id += 1
        is_vip = random.random() < VIP_PROBABILITY  # Determine if the customer is VIP
        env.process(customer_process(env, customer_id, bank, is_vip))

# Run Simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()
bank = BankQueueSimulation(env, NUM_TELLERS, SERVICE_RATE)
env.process(customer_arrivals(env, bank, ARRIVAL_RATE))
env.run(until=SIM_TIME)

# Performance Analysis
print("\n=== Simulation Summary ===")
print(f"Average Wait Time: {np.mean(wait_times):.4f} minutes")

# Visualization of Waiting Times
plt.hist(wait_times, bins=10, color="blue", alpha=0.7)
plt.xlabel("Waiting Time (minutes)")
plt.ylabel("Number of Customers")
plt.title("Customer Waiting Time Distribution")
plt.show()

# Visualization of Teller Utilization
teller_utilization = [(time / SIM_TIME) * 100 for time in bank.teller_usage]
plt.bar(range(1, NUM_TELLERS + 1), teller_utilization, color="green", alpha=0.7)
plt.xlabel("Teller ID")
plt.ylabel("Utilization (%)")
plt.title("Teller Utilization Over Time")
plt.show()
