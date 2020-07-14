import json
import subprocess

from programs.services.processing.Messages import FileDurationAboveFixed, FileDurationBelowLimit, \
    FileDurationAboveLimit, SampleRateBelowMinimum, BitRateBelowMinimum, BitRateBelowRecommended, \
    FileHasClipping, FileNotNormalized, FileDynamicRange


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
        default_params = ["-ar", self.min_sample_rate, "-ac", '2']  # 2 = number of channels

        measured_duration = self.check_duration(float(self.info['duration']) / 60)
        self.check_sample_rate(self.info['sample_rate'])
        self.check_bitrate(self.info['bit_rate'])
        normalization_data = self.check_normalization_clipping()

        if len(self.problems) > 0:
            raise IrrecoverableProblemsException("There are serious problems with the file and it can't be exported.")

        if self.do_normalization:
            print("\t\t* Applying 2 pass loudnorm...")
            loudnorm_list = self.build_loudnorm_list(normalization_data)
            loudnorm_list[-1] += ", " + "atempo=" + str(measured_duration) #Include duration correction
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
             "offset={}").format(
                data["input_i"],
                data["input_lra"],
                data["input_tp"],
                data["input_thresh"],
                data["target_offset"]
            )
        ]
    
    def check_normalization_clipping(self):
        normalization_data = self.read_loudnorm_data()

        #Set a 2dB tolerance for volume
        measured_i = normalization_data["input_i"]
        target_i = -16.0
        tolerance_i = 2.0
        if abs(float(measured_i) - target_i) > tolerance_i:
            self.warnings.append(FileNotNormalized(measured_i, target_i))
        
        #Set dynamic range limit
        measured_lra = normalization_data["input_lra"]
        maximum_lra = 13.0
        if float(measured_lra) > maximum_lra:
            self.warnings.append(FileDynamicRange(measured_lra, 11.0))
        
        #Set true peak normalization
        if float(normalization_data["input_tp"]) >= -0.2:
            self.problems.append(FileHasClipping)

        return normalization_data

    def check_duration(self, measured_duration: float):
        closest_duration = min(self.durations, key=lambda x: abs(x - measured_duration))
        seconds = measured_duration*60
        minutes, seconds = divmod(seconds, 60)
        minutes, seconds = int(minutes), int(seconds)
        measured_duration_display = f'{minutes:02}:{seconds:02}'
        if measured_duration > closest_duration * 1.03:
            self.problems.append(
                FileDurationAboveLimit(measured_duration_display, closest_duration))

        elif measured_duration < closest_duration * 0.8:
            self.problems.append(
                FileDurationBelowLimit(measured_duration_display, closest_duration))

        elif closest_duration * 0.8 <= measured_duration < closest_duration * 0.97:  # Low but accepted.
            return 1

        elif closest_duration * 0.97 <= measured_duration <= closest_duration:  # If we're here, it's within the 3% range.
            return measured_duration / closest_duration

        elif closest_duration < measured_duration <= closest_duration * 1.03:  # If we're here, it's within the 3% range.
            if seconds > 0:
                self.warnings.append(
                    FileDurationAboveFixed(measured_duration_display, closest_duration)
                )
            return measured_duration / closest_duration

        else:
            print("ERROR: Duration is " + str(measured_duration) + " and should be " + str(closest_duration))

    def check_sample_rate(self, measured_samplerate):
        if (measured_samplerate < self.min_sample_rate):
            self.problems.append(SampleRateBelowMinimum(measured_samplerate, self.min_sample_rate))

    def check_bitrate(self, measured_bitrate):
        if self.min_bitrate <= measured_bitrate[:3] < self.recommended_bitrate:
            self.warnings.append(BitRateBelowRecommended(measured_bitrate[:3], self.recommended_bitrate))

        elif self.min_bitrate > measured_bitrate[:3]:
            self.problems.append(BitRateBelowMinimum(measured_bitrate[:3], self.min_bitrate))


class IrrecoverableProblemsException(Exception):
    pass
