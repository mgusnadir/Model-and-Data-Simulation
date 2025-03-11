import simpy
import random
import statistics

# Parameter simulasi
RANDOM_SEED = 42
NUM_AGENTS = 2  # Jumlah agen yang memproses tiket
INTER_ARRIVAL_TIME = 4  # Waktu antar kedatangan pelanggan (rata-rata)
SERVICE_TIME = [3, 7]  # Rentang waktu layanan tiket (min, max)
SIM_TIME = 100  # Durasi simulasi dalam satuan menit

random.seed(RANDOM_SEED)

wait_times = []  # Menyimpan waktu tunggu pelanggan
total_service_time = 0  # Total waktu layanan
total_customers = 0  # Jumlah pelanggan yang dilayani

def customer(env, name, ticket_system):
    """Pelanggan datang, menunggu jika perlu, dan dilayani oleh agen."""
    global total_service_time, total_customers
    
    arrival_time = env.now
    with ticket_system.request() as request:
        yield request  # Menunggu giliran layanan
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        
        service_duration = random.randint(*SERVICE_TIME)
        total_service_time += service_duration
        total_customers += 1
        yield env.timeout(service_duration)  # Waktu pelayanan

def customer_generator(env, ticket_system):
    """Menghasilkan pelanggan baru dalam interval tertentu."""
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / INTER_ARRIVAL_TIME))
        i += 1
        env.process(customer(env, f'Pelanggan {i}', ticket_system))

# Simulasi
env = simpy.Environment()
ticket_system = simpy.Resource(env, capacity=NUM_AGENTS)
env.process(customer_generator(env, ticket_system))
env.run(until=SIM_TIME)

# Analisis hasil
average_wait_time = statistics.mean(wait_times) if wait_times else 0
system_utilization = (total_service_time / (SIM_TIME * NUM_AGENTS)) * 100

print(f'Rata-rata waktu tunggu: {average_wait_time:.2f} menit')
print(f'Utilisasi sistem: {system_utilization:.2f}%')


