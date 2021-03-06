from processing.post_processing import generate_single_track
from utils.constants_parser import get_general_args
from utils.utils import prepare_transformations
import argparse
import torch


def get_track_generation_args():
    """
    Parses the arguments related to the generation of a track if provided by the user, otherwise uses default
    values.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Generates a track from an input .midi file.')
    parser.add_argument('--original_midi',
                        default='/media/thomas/Samsung_T5/VITA/data/maestro-v1.0.0/2015/MIDI-Unprocessed_R1_D1-1-8_mid--AUDIO-from_mp3_04_R1_2015_wav--4.midi',
                        type=str, help='Original .midi file to base the input and target on.')
    parser.add_argument('--temp_dir', default='data/temp', type=str,
                        help='Location of a temporary directory to store temporary files. If is does not exists it will'
                             'be created. If it already exists its content will be erased. After the creation of the '
                             'dataset the temporary folder and its content will be deleted.')
    parser.add_argument('--generator_path', default='objects/generator_trainer_autoencoder.tar', type=str,
                        help='Path to a generator or gan trainer to load pre-trained weights.')
    parser.add_argument('--n_samples', default=300, type=int, help='Number of samples to generate.')
    parser.add_argument('--input_instrument', default=4, type=int, help='Input instrument, default is electric piano.')
    parser.add_argument('--input_velocity', default=None, type=int,
                        help='Velocity corresponds to the volume at which a given key is played. When set to a value in'
                             ' [0, 127] this information is lost.')
    parser.add_argument('--input_control', default=None, type=int,
                        help='Control corresponds to effects (sustain/pedal) applied on the signal. The only control in'
                             ' the Maestro dataset is the pedal which is encoded on value 64. A specific control can be'
                             ' set to a new control value using control and control_value arguments.')
    parser.add_argument('--input_control_value', default=None, type=int,
                        help='The control value is typically set to zero to remove a specific effect selected with the'
                             ' control argument.')
    parser.add_argument('--target_instrument', default=0, type=int, help='Input instrument, default is classic piano.')
    parser.add_argument('--target_velocity', default=None, type=int,
                        help='Velocity corresponds to the volume at which a given key is played. When set to a value in'
                             ' [0, 127] this information is lost.')
    parser.add_argument('--target_control', default=None, type=int,
                        help='Control corresponds to effects (sustain/pedal) applied on the signal. The only control in'
                             ' the Maestro dataset is the pedal which is encoded on value 64. A specific control can be'
                             ' set to a new control value using control and  arguments.')
    parser.add_argument('--target_control_value', default=None, type=int,
                        help='The control value is typically set to zero to remove a specific effect selected with the'
                             ' control argument.')
    args = parser.parse_args()
    return args


def generate_track(general_args, track_args):
    """
    Generates a single track with a pre-trained generator and an input .midi files.
    :param general_args: argument parser storing constants independent of the executed file.
    :param track_args: aurgument parser storing constants related to the track generation.
    :return: None
    """
    generate_single_track(original_midi_filepath=track_args.original_midi,
                          temporary_directory_path=track_args.temp_dir,
                          transformations=prepare_transformations(track_args),
                          generator_path=track_args.generator_path,
                          device=('cuda' if torch.cuda.is_available() else 'cpu'),
                          general_args=general_args,
                          track_args=track_args)


if __name__ == '__main__':
    # Get the parameters related to the track generation
    track_args = get_track_generation_args()

    # Get the general parameters
    general_args = get_general_args()
    generate_track(general_args, track_args)
