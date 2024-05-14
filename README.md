# ECARA
## Evolutionary Context-Aware Recommendation Algorithm

### Overview

The Evolutionary Context-Aware Recommendation Algorithm (ECARA) is a novel recommendation system that leverages evolutionary algorithms and large language models (LLMs) to optimize user selections over time. This algorithm dynamically adjusts its recommendation strategies based on user behavior, context, and feedback, continuously evolving to improve recommendation relevance and user satisfaction.

### Key Features
- **Evolutionary Approach**: Uses evolutionary algorithms to iteratively improve recommendation strategies.
- **LLM Integration**: Employs a large language model (e.g., GPT-4) to analyze feedback and guide the evolution process.
- **Contextual Awareness**: Incorporates real-time context and user behavior data into the recommendation process.
- **Optimization of User Selection**: Focuses on enhancing the likelihood of user selection and satisfaction over time.

### Configuration

1. **OpenAI API Key**:
   Set your OpenAI API key:
   ```python
   openai.api_key = "your_openai_api_key"
   ```

2. **HubSpot API Key**:
   Set your HubSpot API key:
   ```python
   HUBSPOT_API_KEY = "your_hubspot_api_key"
   ```

3. **Customize HubSpot API Request**:
   Update the HubSpot API request URL and parameters in the `fetch_hubspot_data` function to match your specific data needs.

### Usage

The main script for running ECARA is `ecara.py`. This script initializes the recommendation variations, fetches data from HubSpot, updates the variations, and runs the genetic algorithm to optimize the recommendations. It schedules the genetic algorithm to run once every 24 hours.

#### Running the Script
1. Ensure your API keys are set and environment is configured.
2. Run the script:
   ```bash
   python ecara.py
   ```

### Code Structure

- **Initialization**:
  - Set API keys and initialize recommendation variations.
  
- **Data Collection**:
  - `fetch_hubspot_data`: Fetches performance data from HubSpot.
  - `update_recommendation_variations`: Updates the recommendation variations based on fetched data.

- **Evolutionary Algorithm**:
  - `fitness`: Calculates the fitness score for each variation.
  - `roulette_wheel_selection`: Selects parents based on fitness scores.
  - `crossover`: Creates new offspring by combining parent strategies.
  - `request_gpt_optimization`: Sends data to GPT-4 for mutation strategy optimization.
  - `mutate_variation`: Applies the mutation strategy to new offspring.
  - `genetic_algorithm`: Runs the evolutionary algorithm for a specified number of generations.

- **Scheduling**:
  - `schedule_genetic_algorithm`: Schedules the genetic algorithm to run once every 24 hours.

### Example Use Case

**Streaming Service**:
- A user is browsing a streaming service on a Sunday afternoon.
- ECARA collects context data and recent user interactions.
- The algorithm generates an initial population of recommendation strategies.
- Recommendations are presented to the user, and feedback is collected.
- GPT-4 analyzes the feedback, identifies high-performing strategies, and guides the mutation process.
- Over multiple generations, ECARA continuously refines recommendations to better match user preferences and context.

### Potential Challenges

- **Computational Complexity**: Running an evolutionary algorithm with LLM analysis can be computationally intensive.
- **Data Privacy**: Ensuring user data is handled securely and ethically is crucial.
- **Real-Time Processing**: Maintaining real-time performance while evolving recommendation strategies can be challenging.

### Conclusion

ECARA represents a significant advancement in recommendation systems, combining evolutionary algorithms with the analytical power of large language models. By continuously adapting to user behavior and real-time context, ECARA aims to enhance personalization and user satisfaction over time.
