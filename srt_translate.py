import os
import glob

from srtranslator import SrtFile
from srtranslator.translators.translatepy import TranslatePy

def srt_translate(
        in_srt_file,
        out_srt_file,
        from_lang="en",
        to_lang="zh"
    ):
    """
    in_srt_file : 输入 srt
    out_srt_file: 输出 srt
    from_lang   : 输入 srt 语言
    to_lang     : 输出 srt 语言
    """
    translator = TranslatePy()
    srt = SrtFile(in_srt_file)
    srt.translate(translator, from_lang, to_lang)
    srt.wrap_lines()
    srt.save(out_srt_file)
    translator.quit()
    print(f"srt_translate: {out_srt_file}")
    return out_srt_file

def srts_translate(
    srt_dir     = "subtitles",
    from_lang   = "en",
    to_lang     = "zh",
    ):
    """
    srt_dir     : srt 输入和输出目录
    from_lang   : 输入 srt 语言
    to_lang     : 输出 srt 语言
    """
    # 遍历 from_lang 字幕，翻译成 to_lang 字幕
    for in_srt_file in glob.glob(os.path.join(srt_dir, f"**/*-{from_lang}.srt"), recursive=True):
        basename = os.path.basename(in_srt_file).split("-")[0]
        out_srt_file = os.path.join(srt_dir, f"{basename}-{to_lang}.srt")

        srt_translate(
            in_srt_file=in_srt_file,
            out_srt_file=out_srt_file,
            from_lang=from_lang,
            to_lang=to_lang
        )


if __name__ == "__main__":
    srts_translate(
        srt_dir="subtitles",
        from_lang="en",
        to_lang="zh"
    )
