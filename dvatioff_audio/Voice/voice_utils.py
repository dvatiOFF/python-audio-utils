import re
from jiwer import wer
from pypinyin import lazy_pinyin
import Levenshtein
import pykakasi
import numpy as np
import wavio


def generate_sine_wave(frequency=440.0, duration=1, rate=8000):
    """生成一个正弦波形"""
    t = np.linspace(0, duration, int(duration * rate), endpoint=False)
    return np.sin(2 * np.pi * frequency * t)


def save_sine_wave_to_wav(filename, frequency=440.0, duration=1, rate=8000):
    """保存正弦波到.wav文件"""
    sine_wave = generate_sine_wave(frequency, duration, rate)
    wavio.write(filename, sine_wave, rate, sampwidth=3)


def chinese_to_pinyin(text):
    """
    把中文转化为拼音
    """
    lazy_pinyin_text = lazy_pinyin(text)
    sentence = " ".join(lazy_pinyin_text)

    # 将连续的空白字符替换为单个空格
    sentence = re.sub(r'\s+', ' ', sentence)

    return sentence


def japanese_to_kata(text):
    """
    将日文转化为片假名
    """
    kks = pykakasi.kakasi()
    kata_text = kks.convert(text)
    kata = ''

    for item in kata_text:
        kata += item['kana']

    return kata


def japanese_to_romaji(text):
    """
    将日文转化为罗马音
    """
    kks = pykakasi.kakasi()
    kks_text = kks.convert(text)
    romaji = ''

    for item in kks_text:
        romaji += item['hepburn']

    return romaji


def remove_text_within_brackets(text):
    """
    去除文本中括号内的内容，包括括号本身，这里的括号包括半角括号 () 和全角括号 （）和方括号 []
    """
    pattern = re.compile(r'\(.*?\)|（.*?）|\[.*?\]')

    return pattern.sub('', text)


def replace_punctuation_to_space(text):
    """
    去除文本中所有的标点符号
    """
    text = text.replace('\n', '')

    # 正则表达式匹配所有标点符号
    pattern = re.compile(r'[!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~，？！…。、【】；‘’“”·（）—―～「」]')

    text = pattern.sub(' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def replace_punctuation_to_empty(text):
    """
    去除文本中的标点符号
    """

    # 将'\n' 和 ' ' 替换为''
    text = text.replace('\n', '')
    text = text.replace(' ', '')

    # 正则表达式匹配所有标点符号
    pattern = re.compile(r'[!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~，？！…。、【】；‘’“”·（）—―「」]')
    text = pattern.sub('', text)

    return text


def remove_all_space(text):
    """
    去除文本中的所有空格
    """
    text = text.replace(' ', '')

    return text


def text_distance(text1, text2):
    """
    计算两个文本之间的 Levenshtein 距离
    """
    distance = Levenshtein.distance(text1, text2)

    return distance


def text_wrong_proportion(text1, text2):
    """
    使用 Jiwer 计算两个字符串之间的词错误率
    """
    proportion = wer(text1, text2)

    return proportion
