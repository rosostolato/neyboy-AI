from pynn import Neural_Network
import pickle


class Gentic_Evolution:
    def __init__(self, pop_length):
        """Create a population of random networks.
        Args:
            pop_length (int): Number of networks to generate, aka the
                size of the population
        """
        self.population = []

        for _ in range(0, pop_length):
            # Create a random network.
            network = Neural_Network(2, 6, 1)
            network.create_random()

            # Add the network to our population.
            self.population.append(network)

    def from_file(self, filename):
        with open(filename, "rb") as f:
            arr = pickle.load(f)
            self.renew_generation(arr[1], arr[2])

    def renew_generation(self, father, mother):
        """Make two children as parts of their parents.
        Args:
            father (dict): Network parameters
            mother (dict): Network parameters
        """
        newgen = [father, mother]

        for i in range(len(self.population) - 3):
            network = Neural_Network(2, 6, 1)
            network.create_from_parents(father, mother, i)

            newgen.append(network)

        # Create a random network.
        for i in range(1):
            network = Neural_Network(2, 6, 1)
            network.create_random()

            # Add the network to our population.
            newgen.append(network)

        self.population = newgen
