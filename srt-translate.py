import os
import glob

from srtranslator import SrtFile
from srtranslator.translators.translatepy import TranslatePy

def srt_translate(
    srt_dir     = "subtitles",
    from_lang   = "en",
    to_lang     = "zh",
    ):
    """
    srt_dir     : srt 输入和输出目录
    from_lang   : 输入 srt 语言
    to_lang     : 输出 srt 语言
    """
    translator = TranslatePy()
    for in_srt_file in glob.glob(os.path.join(srt_dir, f"**/*-{from_lang}.srt"), recursive=True):
        srt = SrtFile(in_srt_file)
        srt.translate(translator, from_lang, to_lang)
        srt.wrap_lines()

        basename = os.path.basename(in_srt_file).split("-")[0]
        out_srt_file = os.path.join(srt_dir, f"{basename}-{to_lang}.srt")
        srt.save(out_srt_file)
        print(f"srt-translate output: {out_srt_file}")
    translator.quit()


if __name__ == "__main__":
    srt_translate(
        srt_dir="subtitles",
        from_lang="en",
        to_lang="zh"
    )
