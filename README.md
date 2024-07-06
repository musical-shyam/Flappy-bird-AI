# Flappy-bird-AI
## Rahat Rahman & Shyam Kannan
### How to Run the Project

1. Clone or download the repository <br />
2. To install necessary libraries: `pip install -r requirements.txt` <br />
3. To run the program in the terminal: `python main.py` or `python3 main.py` <br />

<br /> If there is an issue, try clearing `__pycache__` <br />

### Problem Statement

  In the realm of artificial intelligence and game development, creating intelligent agents that can adapt and respond to dynamic environments is a pivotal challenge. Flappy Bird, a game characterized by its simplicity and the dynamic nature of its gameplay, provides an ideal platform for exploring machine learning algorithms. The primary objective of this project is to **develop an AI that can proficiently play Flappy Bird by autonomously navigating through the series of obstacles** presented in the game. To achieve this, we propose the implementation of a neural network model, specifically a single-layer perceptron, which is a foundational building block in neural network theory.

  However, the conventional training methods for neural networks, such as the gradient descent algorithms, may not be directly applicable or efficient for a game like Flappy Bird where the learning feedback is discontinuous and binary (either the bird passes through the gap or it doesn’t). To address this, we turn to an alternative approach using the Neuroevolution Fixed Topologies(NEFT) genetic algorithm. This algorithm offers a robust method to optimize the perceptron by treating the problem as one of evolutionary survival, where only the best-performing AI through successive generations is developed.

  This project aims to **explore the effectiveness of the NEFT genetic algorithm** in rapidly evolving a perceptron that can handle the game’s requirements. By focusing on this method, we anticipate not only achieving a high level of play but also demonstrating the feasibility of using genetic algorithms for training neural networks in settings where traditional backpropagation is less effective. The successful implementation of this project could provide insights into the broader applicability of genetic algorithms in neural network training, particularly in real-time decision-making scenarios.

For more details about the project, read the project report pdf added to the repository.
