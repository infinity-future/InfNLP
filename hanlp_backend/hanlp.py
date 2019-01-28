
import re
import os
from jpype import getDefaultJVMPath, startJVM, JClass

BASE_CWD = os.getcwd()
CURRENT_DIR = os.path.realpath(os.path.dirname(__file__))
properies_sample = open(
    os.path.join(CURRENT_DIR, 'hanlp.properties.sample')).read()
with open(os.path.join(CURRENT_DIR, 'hanlp.properties'), 'w') as fp:
    fp.write(properies_sample.format(PATH=CURRENT_DIR))


def chcwd(origin_func):
    """修改当前工作目录"""
    def wrapper(self, *args, **kwargs):
        os.chdir(self.module_path)
        u = origin_func(self, *args, **kwargs)
        os.chdir(BASE_CWD)
        return u
    return wrapper


class HanLP(object):
    """HanLP的封装"""
    module_path = os.path.abspath(os.path.dirname(__file__))
    java_class_path = os.path.join(module_path, 'hanlp.jar') + \
        ':' + module_path

    @chcwd
    def __init__(self):
        # try:
        startJVM(
            getDefaultJVMPath(),
            '-Djava.class.path=' + self.java_class_path,
            '-Xms1g', '-Xmx1g')
        # attachThreadToJVM()
        # except:
        #     pass
        self._hanlp = JClass('com.hankcs.hanlp.HanLP')

    @chcwd
    def pos(self, content, engine='StandardTokenizer'):
        return self.tokenize(content, no_pos=False, engine=engine)

    @chcwd
    def tokenize(self, content, no_pos=True, engine='StandardTokenizer'):
        """分词
        StandardTokenizer
        IndexTokenizer
        SpeedTokenizer
        """
        if isinstance(content, str) and len(content) > 0:
            segments = []
            if engine == 'StandardTokenizer':
                tokenizer = JClass(
                    'com.hankcs.hanlp.tokenizer.StandardTokenizer')
            elif engine == 'IndexTokenizer':
                tokenizer = JClass(
                    'com.hankcs.hanlp.tokenizer.IndexTokenizer')
            elif engine == 'SpeedTokenizer':
                tokenizer = JClass(
                    'com.hankcs.hanlp.tokenizer.SpeedTokenizer')
            else:
                raise RuntimeError('Invalid Tokenize Engine')
            ret = tokenizer.segment(content)
            # print(content, ret)
            for v in ret:
                if no_pos:
                    segments.append(re.sub(r'/[a-zA-Z0-9]+$', '', str(v)))
                else:
                    segments.append(str(v))
            return segments

    @chcwd
    def extract_keywords(self, content, number=5):
        """提取关键字
        """
        hanlp = JClass('com.hankcs.hanlp.summary.TextRankKeyword')
        ret = hanlp.getKeywordList(content, number)
        segments = []
        for v in ret:
            segments.append(str(v))
        return segments

    @chcwd
    def extract_summary(self, content, number=5):
        """提取关键句子，即摘要
        """
        hanlp = JClass('com.hankcs.hanlp.summary.TextRankSentence')
        ret = hanlp.getTopSentenceList(content, number)
        segments = []
        for v in ret:
            segments.append(str(v))
        return segments

    @chcwd
    def extract_phrase(self, content, number=5):
        """提取互信息短句
        """
        hanlp = JClass((
            'com.hankcs.hanlp.mining.'
            'phrase.'
            'MutualInformationEntropyPhraseExtractor'))
        ret = hanlp.extract(content, number)
        segments = []
        for v in ret:
            segments.append(str(v))
        return segments

    @chcwd
    def parse(self, content):
        """
        MaxEntDependencyParser
        NeuralNetworkDependencyParser
        """

        def _extract_word(word):
            w = {}
            for attr in ('ID', 'LEMMA', 'POSTAG', 'DEPREL'):
                w[attr.lower()] = getattr(word, attr)
            return w

        hanlp = JClass((
            'com.hankcs.hanlp.'
            'dependency.nnparser.NeuralNetworkDependencyParser'))
        tokenizer = JClass(
            'com.hankcs.hanlp.tokenizer.StandardTokenizer')
        r = hanlp.compute(tokenizer.segment(content))
        ret = []
        for word in r.getWordArray():
            w = _extract_word(word)
            w['head'] = _extract_word(word.HEAD)['id']
            ret.append(w)
        return ret

    @chcwd
    def add(self, word):
        hanlp = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
        hanlp.add(word)

    @chcwd
    def insert(self, word, info):
        hanlp = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
        hanlp.insert(word, info)

    @chcwd
    def pinyin(self, content, method='default'):
        hanlp = JClass('com.hankcs.hanlp.HanLP')
        ret = hanlp.convertToPinyinList(content)
        segments = []
        # import pdb; pdb.set_trace()
        for v in ret:
            if method == 'with_tone':
                # ['wǒ', 'ài', 'běi', 'jīng', 'tiān', 'ān', 'mén']
                segments.append(v.getPinyinWithToneMark())
            elif method == 'without_tone':
                # ['wo', 'ai', 'bei', 'jing', 'tian', 'an', 'men']
                segments.append(v.getPinyinWithoutTone())
            elif method == 'tone':
                # [3, 4, 3, 1, 1, 1, 2]
                segments.append(v.getTone())
            else:  # default
                # ['wo3', 'ai4', 'bei3', 'jing1', 'tian1', 'an1', 'men2']
                segments.append(v.toString())
        return segments

    @chcwd
    def s2t(self, content):
        hanlp = JClass('com.hankcs.hanlp.HanLP')
        return hanlp.convertToTraditionalChinese(content)

    @chcwd
    def t2s(self, content):
        hanlp = JClass('com.hankcs.hanlp.HanLP')
        return hanlp.convertToSimplifiedChinese(content)
