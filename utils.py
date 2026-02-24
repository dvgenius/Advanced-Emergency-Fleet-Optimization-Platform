import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_incidents(n=50):
    np.random.seed(42) 
    incidents = []
    types = ['Medical', 'Fire', 'Traffic Accident', 'Hazardous Material']
    severities = ['Low', 'Medium', 'High', 'Critical']
    statuses = ['Active', 'En Route', 'Resolved']
    locations = ["Connaught Place", "India Gate", "Chandni Chowk", "Lajpat Nagar", "Karol Bagh", "Hauz Khas", "Vasant Kunj", "Saket", "Dwarka", "Rohini", "Janakpuri", "Laxmi Nagar", "Okhla", "Kalkaji", "Pitampura", "Rajouri Garden", "Greater Kailash", "Defense Colony", "Green Park", "Mayur Vihar", "Noida Sector 18", "Gurugram Cyber Hub", "Faridabad NIT", "Ghaziabad Indirapuram"]
    
    
    base_lat, base_lon = 28.6139, 77.2090
    
    for i in range(n):
        incidents.append({
            'ID': f'INC-{1000+i}',
            'Type': np.random.choice(types),
            'Location': np.random.choice(locations),
            'Severity': np.random.choice(severities, p=[0.2, 0.4, 0.3, 0.1]),
            'Status': np.random.choice(statuses, p=[0.6, 0.3, 0.1]),
            'Lat': base_lat + np.random.uniform(-0.1, 0.1),
            'Lon': base_lon + np.random.uniform(-0.1, 0.1),
            'Time_Reported': (datetime.now() - timedelta(minutes=int(np.random.randint(5, 120)))).strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(incidents)

def generate_mock_responders(n=20):
    np.random.seed(24)
    responders = []
    types = ['Ambulance', 'Fire Truck', 'Rapid Response Vehicle']
    statuses = ['Available', 'Dispatched', 'Maintenance']
   
    base_lat, base_lon = 28.6139, 77.2090
    
    for i in range(n):
        responders.append({
            'ID': f'RES-{2000+i}',
            'Type': np.random.choice(types),
            'Status': np.random.choice(statuses, p=[0.7, 0.2, 0.1]),
            'Lat': base_lat + np.random.uniform(-0.1, 0.1),
            'Lon': base_lon + np.random.uniform(-0.1, 0.1)
        })
    return pd.DataFrame(responders)
