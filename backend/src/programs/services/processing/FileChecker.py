import json
import subprocess

from programs.services.processing.Messages import FileDurationAboveFixed, FileDurationBelowLimit, \
    FileDurationAboveLimit, SampleRateBelowMinimum, BitRateBelowMinimum, BitRateBelowRecommended


class FileChecker:
    """
    Checks the specified media file for problems with technical details, such as a bad sample or bit rate, duration,
    etc...
    Returns a parameters string for export, or error if there are problems.
    """

    def __init__(self, file_path, durations, min_sample_rate, min_bitrate, recommended_bitrate, info, do_normalization):
        self.do_normalization = do_normalization
        self.info = info
        self.recommended_bitrate = recommended_bitrate
        self.min_bitrate = min_bitrate
        self.min_sample_rate = min_sample_rate
        self.durations = durations
        self.file_path = file_path
        self.problems = []
        self.warnings = []

    def run_checks(self):
        default_params = ["-ar", self.min_sample_rate, "-ac", 2]  # 2 = number of channels

        tempo = self.check_duration(float(self.info['duration']) / 60)
        self.check_sample_rate(self.info['sample_rate'])
        self.check_bitrate(self.info['bit_rate'])

        if len(self.problems) > 0:
            raise IrrecoverableProblemsException("There are serious problems with the file and it can't be exported.")

        if self.do_normalization:
            loudnorm_list = self.build_loudnorm_list(self.read_loudnorm_data())
            loudnorm_list[-1] += "," + str(tempo)
            return default_params + loudnorm_list
        else:
            return default_params

    def can_export(self) -> bool:
        return len(self.problems) == 0

    def read_loudnorm_data(self) -> dict:
        """ Reads necessary info from the file so that the Loudnorm normalization
        is more accurate. 1st step of *Loudnorm 2 pass*.
        See: http://k.ylo.ph/2016/04/04/loudnorm.html
        Returns:
            loudnorm_data: Contains the measured parameters to be used
                as "measured_X" in the 2nd pass.
        """

        command = ["ffmpeg", "-i", self.file_path, "-af",
                   "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]
        p = subprocess.Popen(command, stderr=subprocess.PIPE).stderr.read()
        subs = p[-300:]  # "Big enough" to contain the JSON. Has extra info.

        # Finding the start of the JSON
        for i, c in enumerate(subs):
            if c == ord("{"):
                subs = subs[i:]

        loudnorm_data = json.loads(subs.decode('utf-8'))
        return loudnorm_data

    def build_loudnorm_list(self, data):
        return [
            "-ac", "2", "-c:v", "copy", "-af:a",
            ("loudnorm=dual_mono=true:I=-16:TP=-1.5:LRA=11:"
             "measured_I={}:"
             "measured_LRA={}:"
             "measured_TP={}:"
             "measured_thresh={}:"
             "offset={}:linear=true").format(
                data["input_i"],
                data["input_lra"],
                data["input_tp"],
                data["input_thresh"],
                data["target_offset"]
            )
        ]

    def check_duration(self, measured_duration: float):
        closest_duration = min(self.durations, key=lambda x: abs(x - measured_duration))

        if measured_duration > closest_duration * 1.03:
            self.problems.append(
                FileDurationAboveLimit(measured_duration, closest_duration))

        elif measured_duration < closest_duration * 0.8:
            self.problems.append(
                FileDurationBelowLimit(measured_duration, closest_duration))

        elif closest_duration * 0.8 <= measured_duration < closest_duration * 0.97:  # Low but accepted.
            return 1

        elif closest_duration * 0.97 <= measured_duration <= closest_duration:  # If we're here, it's within the 3% range.
            return measured_duration / closest_duration

        elif closest_duration < measured_duration <= closest_duration * 1.03:  # If we're here, it's within the 3% range.
            self.problems.append(
                FileDurationAboveFixed(measured_duration, closest_duration)
            )
            return measured_duration / closest_duration

        else:
            print("ERROR: Duration is " + str(measured_duration) + " and should be " + str(closest_duration))

    def check_sample_rate(self, measured_samplerate):
        if (measured_samplerate < self.min_sample_rate):
            self.problems.append(SampleRateBelowMinimum(measured_samplerate, self.min_sample_rate))

    def check_bitrate(self, measured_bitrate):
        if self.min_bitrate <= measured_bitrate[:3] < self.recommended_bitrate:
            self.warnings.append(BitRateBelowRecommended(measured_bitrate, self.recommended_bitrate))

        elif self.min_bitrate > measured_bitrate[:3]:
            self.problems.append(BitRateBelowMinimum(measured_bitrate, self.min_bitrate))


class IrrecoverableProblemsException(Exception):
    pass
