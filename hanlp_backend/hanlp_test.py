import unittest
from .hanlp import HanLP

nlp = HanLP()


class TestHanlp(unittest.TestCase):

    def test_tokenizer(self):

        r = nlp.tokenize('我爱北京天安门', engine='StandardTokenizer')
        self.assertEqual(' '.join(r), ' '.join(['我', '爱', '北京', '天安门']))

        r = nlp.tokenize('我爱北京天安门', engine='IndexTokenizer')
        self.assertEqual(' '.join(r), ' '.join(['我', '爱', '北京', '天安门', '天安']))

        r = nlp.tokenize('我爱北京天安门', engine='SpeedTokenizer')
        self.assertEqual(' '.join(r), ' '.join(['我', '爱', '北京', '天安门']))

        nlp.add('北京天安门')

        r = nlp.tokenize('我爱北京天安门', engine='StandardTokenizer')
        self.assertEqual(' '.join(r), ' '.join(['我', '爱', '北京天安门']))

        nlp.add('我爱')

        r = nlp.tokenize('我爱北京天安门', engine='StandardTokenizer')
        self.assertEqual(' '.join(r), ' '.join(['我爱', '北京天安门']))

        # print(nlp.extract_keywords('我爱北京天安门'))
        with self.assertRaises(RuntimeError):
            nlp.tokenize('我爱北京天安门', engine='BadEngine')

    def test_extract_keywords(self):
        r = nlp.extract_keywords('我爱北京天安门')
        self.assertEqual(
            ' '.join(r),
            ' '.join(['天安门', '北京', '爱'])
        )

    def test_pos(self):
        r = nlp.pos('我爱北京天安门')
        self.assertEqual(
            ' '.join(r),
            ' '.join(['我/rr', '爱/v', '北京/ns', '天安门/ns'])
        )

    def test_parse(self):
        ret = nlp.parse('我爱北京天安门')
        print(ret)

        sample_output = [{'id': 1, 'lemma': '我', 'postag': 'rr', 'deprel': 'SBV', 'head': 2}, {'id': 2, 'lemma': '爱', 'postag': 'v', 'deprel': 'HED', 'head': 0}, {
            'id': 3, 'lemma': '北京', 'postag': 'ns', 'deprel': 'ATT', 'head': 4}, {'id': 4, 'lemma': '天安门', 'postag': 'ns', 'deprel': 'VOB', 'head': 2}]
        self.assertEqual(len(ret), len(sample_output))
        for r, s in zip(ret, sample_output):
            self.assertEqual(r['id'], s['id'])
            self.assertEqual(r['deprel'], s['deprel'])

    def test_pinyin(self):
        ret = nlp.pinyin('我爱北京天安门')
        self.assertEqual(
            ' '.join(ret),
            ' '.join(['wo3', 'ai4', 'bei3', 'jing1', 'tian1', 'an1', 'men2'])
        )

    def test_s2t(self):
        ret = nlp.s2t('用笔记本电脑写程序')
        self.assertEqual('用筆記本電腦寫程序', ret)

    def test_t2s(self):
        ret = nlp.t2s('用筆記本電腦寫程序')
        self.assertEqual('用笔记本电脑写程序', ret)


if __name__ == '__main__':
    unittest.main()
