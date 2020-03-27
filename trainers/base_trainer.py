import abc
import torch


class Trainer(abc.ABC):
    def __init__(self, train_generator, test_generator, valid_generator, savepath):
        # Device
        self.device = ('cuda' if torch.cuda.is_available() else 'cpu')

        # Data generators
        self.train_generator = train_generator
        self.test_generator = test_generator
        self.valid_generator = valid_generator

        # Path to save to the class
        self.savepath = savepath

        # Epoch counter
        self.epoch_counter = 0

        # Stored losses
        self.train_losses = []
        self.test_losses = []
        self.valid_losses = []

    def save(self):
        """
        Saves the complete trainer class
        :return: None
        """
        torch.save(self, self.savepath)

    def generate_single_test_batch(self, model):
        model.eval()
        with torch.no_grad():
            local_batch = next(iter(self.test_generator))
            x_h_batch, x_l_batch = local_batch[0].to(self.device), local_batch[1].to(self.device)
            fake_batch = model(x_l_batch)
        return x_h_batch, fake_batch

    @abc.abstractmethod
    def train(self, epochs):
        """
        Trains the model for a specified number of epochs on the train dataset
        :param epochs: Number of iterations over the complete dataset to perform
        :return: None
        """

    @abc.abstractmethod
    def eval(self, epoch):
        """
        Evaluates the model on the test dataset
        :param epoch: Current epoch, used to print status information
        :return: None
        """

    @abc.abstractmethod
    def plot_reconstruction_time_domain(self, index):
        """
        Plots real samples against fake sample in time domain
        :param index: index of the batch in the test generator to use
        :return: None
        """

    @abc.abstractmethod
    def plot_reconstruction_time_domain(self, index):
        """
        Plots real samples against fake sample in frequency domain
        :param index:
        :return:
        """