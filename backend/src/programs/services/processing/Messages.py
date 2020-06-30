from abc import ABC, abstractmethod


class Message(ABC):
    def __init__(self, measured_value=None, recommended_value=None):
        self.measured_value = measured_value
        self.recommended_value = recommended_value

    @abstractmethod
    def message(self):
        pass


class BitRateBelowRecommended(Message):
    def message(self):
        return "O bitrate do ficheiro da emissão é de {0}, e está " \
               "abaixo dos {1} kbps, o que compromete um pouco a qualidade do áudio. " \
               "Ainda assim, a emissão está pronta a ir para o ar. Na próxima emissão, " \
               "certifica-te que exportas o ficheiro com um bitrate de {1} kbps.".format(self.measured_value,
                                                                                         self.recommended_value)


class BitRateBelowMinimum(Message):
    def message(self):
        return "O bitrate do ficheiro é de {}, estando abaixo dos {} kbps, o que " \
               "compromete seriamente a qualidade do áudio. Verifica se o episódio foi " \
               "exportado com as definições correctas. Se não, grava novamente o " \
               "episódio.".format(self.measured_value,
                                  self.recommended_value)


class SampleRateBelowMinimum(Message):
    def message(self):
        return "A frequência de amostragem (sampling rate) do ficheiro é de {}, e está " \
               "abaixo dos {} Hz, o que compromete seriamente a qualidade do áudio. " \
               "Verifica se o episódio foi exportado com as definições correctas. " \
               "Se não, grava novamente o episódio.".format(self.measured_value,
                                                            self.recommended_value)


class FileDurationAboveLimit(Message):
    def message(self):
        return "A emissão tinha {0} minutos, estando acima dos {1} minutos, o que " \
               "impossibilita o ajuste automático. Por favor, edita o ficheiro " \
               "para um máximo de {1} minutos e envia de novo.".format(self.measured_value,
                                                                       self.recommended_value)


class FileDurationBelowLimit(Message):
    def message(self):
        return "A emissão tinha {0} minutos, estando abaixo da duração mínima definida para um " \
               "programa de {1} minutos e o ficheiro foi automaticamente " \
               "recusado. Por favor, adiciona conteúdo ao programa até ficar com um " \
               "máximo de {1} minutos e envia de novo.".format(self.measured_value,
                                                               self.recommended_value)


class FileDurationAboveFixed(Message):
    def message(self):
        return "O ficheiro da emissão tinha {0} minutos, estando acima dos " \
               "{1} minutos, mas foi ajustada automaticamente e está pronta para ir " \
               "para o ar. Não precisas de fazer mais nada.".format(self.measured_value,
                                                                    self.recommended_value)

class FileHasClipping(Message):
    def message(self):
        return "O ficheiro da emissão possuia clipping, ou seja, um pico acima do volume " \
                "máximo da transmissão. Assegure-se que quando faz a gravação, e durante " \
                "a mistura, não excede o volume máximo (0 dB). Por favor, remistura o teu " \
                "ficheiro de forma a que não existam estes picos e envia de novo."

class FileNotNormalized(Message):
    def message(self):
        return "O ficheiro da emissão tinha um volume de som medido de {0} dB LUFS, que se " \
                "afasta do volume de som indicado para emissão, que é {1} dB LUFS, mas foi " \
                "ajustado automaticamente e está pronto a ir ao ar. Não precisas de fazer " \
                "mais nada.".format(self.measured_value, self.recommended_value)

class FileDynamicRange(Message):
    def message(self):
        return "O ficheiro de emissão tinha uma dinâmica de som de {0} dB (variação de volume " \
                "entre partes altas e silenciosas) que é superior a {1} dB indicado para a emissão, " \
                "mas foi ajustada automaticamente e está pronto a ir ao ar. Não precisas de fazer " \
                "mais nada.".format(self.measured_value, self.recommended_value)
