import random
import openai
import time
import requests

# OpenAI API key
openai.api_key = "your_openai_api_key"

# HubSpot API credentials
HUBSPOT_API_KEY = "your_hubspot_api_key"
HUBSPOT_BASE_URL = "https://api.hubapi.com"

# Define the recommendation variations and their initial performance scores
recommendation_variations = [
    {'id': 1, 'strategy': {'type': 'collaborative', 'params': {}}, 'score': 0, 'impressions': 0, 'clicks': 0},
    {'id': 2, 'strategy': {'type': 'content', 'params': {}}, 'score': 0, 'impressions': 0, 'clicks': 0},
    {'id': 3, 'strategy': {'type': 'contextual', 'params': {}}, 'score': 0, 'impressions': 0, 'clicks': 0},
    {'id': 4, 'strategy': {'type': 'hybrid', 'params': {}}, 'score': 0, 'impressions': 0, 'clicks': 0},
]

def fetch_hubspot_data():
    # Function to fetch performance data from HubSpot
    url = f"{HUBSPOT_BASE_URL}/reports/v2/reports?"
    params = {
        'hapikey': HUBSPOT_API_KEY,
        'dateRange': 'LAST_30_DAYS',
        'metrics': ['impressions', 'clicks'],
        'dimensions': ['strategyType']
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def update_recommendation_variations(data):
    # Update recommendation variations with the data fetched from HubSpot
    for row in data['results']:
        strategy_type = row['strategyType']
        impressions = row['impressions']
        clicks = row['clicks']
        for variation in recommendation_variations:
            if variation['strategy']['type'] == strategy_type:
                variation['impressions'] += impressions
                variation['clicks'] += clicks
                variation['score'] = variation['clicks'] / variation['impressions'] if variation['impressions'] > 0 else 0

def fitness(variation):
    return variation['score']

def roulette_wheel_selection(population):
    max_value = sum(fitness(v) for v in population)
    pick = random.uniform(0, max_value)
    current = 0
    for variation in population:
        current += fitness(variation)
        if current > pick:
            return variation
    return population[-1]

def selection(population):
    parent1 = roulette_wheel_selection(population)
    parent2 = roulette_wheel_selection(population)
    return parent1, parent2

def crossover(parent1, parent2):
    child = {'id': len(recommendation_variations) + 1}
    child['strategy'] = {
        'type': parent1['strategy']['type'] if random.random() < 0.5 else parent2['strategy']['type'],
        'params': parent1['strategy']['params'] if random.random() < 0.5 else parent2['strategy']['params']
    }
    return child

def request_gpt_optimization(data, generation_score):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"Optimize the mutation process for the next generation based on the following data: {json.dumps(data)} and the current generation score: {generation_score}. Your goal is to increase the score for the next generation.",
        max_tokens=200,
    )
    return json.loads(response.choices[0].text.strip())

def mutate_variation(variation, mutation_strategy):
    if 'type' in mutation_strategy:
        variation['strategy']['type'] = mutation_strategy['type']
    if 'params' in mutation_strategy:
        variation['strategy']['params'] = mutation_strategy['params']
    return variation

def genetic_algorithm(population, generations):
    for generation in range(generations):
        # Fetch and update data from HubSpot
        data = fetch_hubspot_data()
        update_recommendation_variations(data)

        # Calculate the current generation's average score
        generation_score = sum(fitness(var) for var in population) / len(population)
        
        # Send the current generation's data and score to GPT-4 for mutation optimization
        data_to_send = [{'id': var['id'], 'strategy': var['strategy'], 'score': var['score']} for var in population]
        mutation_strategy = request_gpt_optimization(data_to_send, generation_score)
        
        new_population = sorted(population, key=fitness, reverse=True)[:2]  # Elitism: preserve top 2
        while len(new_population) < len(population):
            parent1, parent2 = selection(population)
            child = crossover(parent1, parent2)
            child = mutate_variation(child, mutation_strategy)
            new_population.append(child)
        population = new_population
        print(f"Generation {generation + 1}: {population}")
    return population

# Function to run the genetic algorithm once every 24 hours
def schedule_genetic_algorithm():
    while True:
        time.sleep(10 * 60)  # Wait for 10 minutes to ensure data from HubSpot is updated
        optimized_variations = genetic_algorithm(recommendation_variations, generations=1)

        # Print the optimized recommendation variations for the current day
        for variation in optimized_variations:
            print(f"ID: {variation['id']}, Strategy: {variation['strategy']}, Score: {variation['score']}, Impressions: {variation['impressions']}, Clicks: {variation['clicks']}")

        time.sleep(24 * 60 * 60 - 10 * 60)  # Wait for the next 24 hours period

# Start the scheduled genetic algorithm
schedule_genetic_algorithm()
