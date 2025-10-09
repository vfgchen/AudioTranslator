from os import path

from sensevoice_audio_to_srt import load_models
from sensevoice_audio_to_srt import audio_to_srt


if __name__ == "__main__":
    vad_model, asr_model = load_models(
        model_dir       = "./models",
        lang            = "en",
        vad_model_dir   = "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        asr_model_dir   = "iic/SenseVoiceSmall"
    )

    root_dir = "D:/output"
    wav_file = path.join(root_dir, "104-en.wav")
    srt_file = path.join(root_dir, "104-en.srt")

    audio_to_srt(
        wav_file    = wav_file,
        srt_file    = srt_file,
        vad_model   = vad_model,
        asr_model   = asr_model,
    )
