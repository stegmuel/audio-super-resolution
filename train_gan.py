from utils.constants_parser import get_general_args
from trainers.gan_trainer import GanTrainer
from utils.utils import prepare_maestro_data
import argparse


def get_gan_trainer_args():
    """
    Parses the arguments related to the training of the gan if provided by the user, otherwise uses default values.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Trains the GAN.')
    # Data related constants
    parser.add_argument('--use_npy', default=True, type=bool,
                        help='Flag indicating if the data is stored as multiple .npy files or a single .hdf5 file.')
    parser.add_argument('--hdf5_filepath', type=str, help='Location of the .hdf5 file if this data format is selected.')
    parser.add_argument('--train_npy_filepath', default='data/train.npy', type=str,
                        help='Location of the train .npy file if this data format is selected.')
    parser.add_argument('--test_npy_filepath', default='data/test.npy', type=str,
                        help='Location of the test .npy file if this data format is selected.')
    parser.add_argument('--valid_npy_filepath', default='data/valid.npy', type=str,
                        help='Location of the valid .npy file if this data format is selected.')
    parser.add_argument('--train_batch_size', default=64, type=int,
                        help='Number of samples per batch during the train phase.')
    parser.add_argument('--test_batch_size', default=64, type=int,
                        help='Number of samples per batch during the test phase.')
    parser.add_argument('--valid_batch_size', default=64, type=int,
                        help='Number of samples per batch during the validation phase.')
    parser.add_argument('--train_shuffle', default=True, type=bool,
                        help='Flag indicating if the train data must be shuffled.')
    parser.add_argument('--test_shuffle', default=True, type=bool,
                        help='Flag indicating if the test data must be shuffled.')
    parser.add_argument('--valid_shuffle', default=True, type=bool,
                        help='Flag indicating if the validation data must be shuffled.')
    parser.add_argument('--num_worker', default=2, type=int, help='Number of workers used by the data loaders.')

    # Trainer related constants
    parser.add_argument('--savepath', default='/content/drive/My Drive/audio_objects/generator_trainer_autoencoder.tar',
                        type=str,
                        help='Location where to save the gan trainer to resume training.')
    parser.add_argument('--loadpath', default='objects/generator_trainer_autoencoder.tar', type=str,
                        help='Location of an existing gan trainer from which to resume training.')
    parser.add_argument('--use_adversarial', default=True, type=bool,
                        help='Flag indicating whether or not the adversarial criterion should be used')
    parser.add_argument('--lambda_adversarial', default=1e-3, type=float,
                        help='Weight given to the adversarial loss during the GAN training.')
    parser.add_argument('--lambda_freq', default=0., type=float,
                        help='Weight given to the l2 loss in frequency domain during the GAN training.')
    parser.add_argument('--lambda_autoencoder', default=1e-1, type=float,
                        help='Weight given to the l2 loss in the autoencoder embedding space during the GAN training.')
    parser.add_argument('--epochs', default=10, type=int, help='Number of epochs to train the models on.')

    # Autoencoder related constants
    parser.add_argument('--autoencoder_path', default='/content/drive/My Drive/audio_objects/autoencoder_trainer_new.tar',
                        type=str,
                        help='Location of a pre-trained auto-encoder used to extract features from the samples. If not '
                             'provided the gan will be trained without the auto-encoder loss.')

    # Generator related constants
    parser.add_argument('--generator_path', default=None, type=str,
                        help='Location of a pre-trained generator used to generate the samples. If not provided, a new '
                             'generator will be instantiated and trained from scratch. Providing a pre-trained '
                             'generator can help stabilizing the training.')
    parser.add_argument('--generator_lr', default=1e-3, type=float, help='Learning rate for the generator.')
    parser.add_argument('--generator_scheduler_step', default=30, type=int,
                        help='Number of steps before the learning step is reduced by a factor gamma.')
    parser.add_argument('--generator_scheduler_gamma', default=0.5, type=float,
                        help='Factor by which the learning rate is reduced after a specified number of steps.')

    # Discriminator related constants
    parser.add_argument('--discriminator_lr', default=1e-3, type=float, help='Learning rate for the discriminator.')
    parser.add_argument('--discriminator_scheduler_step', default=30, type=int,
                        help='Number of steps before the learning step is reduced by a factor gamma.')
    parser.add_argument('--discriminator_scheduler_gamma', default=0.5, type=float,
                        help='Factor by which the learning rate is reduced after a specified number of steps.')
    args = parser.parse_args()
    return args


def get_gan_trainer(general_args, trainer_args):
    """
    Instantiates the GanTrainer class based on the given arguments.
    :param general_args: instance of an argument parser that stores generic parameters.
    :param trainer_args: instance of an argument parser that stores parameters related to the training.
    :return: instance of an GanTrainer.
    """
    train_loader, test_loader, valid_loader = prepare_maestro_data(trainer_args)

    # Load the train class which will automatically resume previous state from 'loadpath'
    gan_trainer = GanTrainer(train_loader=train_loader,
                             test_loader=test_loader,
                             valid_loader=valid_loader,
                             general_args=general_args,
                             trainer_args=trainer_args)
    return gan_trainer


if __name__ == '__main__':
    # Get the parameters related to the track generation
    trainer_args = get_gan_trainer_args()

    # Get the general parameters
    general_args = get_general_args()

    # Get the trainer
    gan_trainer = get_gan_trainer(general_args, trainer_args)

    # Start training
    gan_trainer.train(epochs=trainer_args.epochs)