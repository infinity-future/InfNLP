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

        sample_output = [
            {
                "CPOSTAG": "d",
                "DEPREL": "主谓关系",
                "ID": 1,
                "LEMMA": "我",
                "NAME": "我",
                "POSTAG": "d",
                "HEAD": 2
            },
            {
                "CPOSTAG": "v",
                "DEPREL": "核心关系",
                "ID": 2,
                "LEMMA": "爱",
                "NAME": "爱",
                "POSTAG": "v",
                "HEAD": 0
            },
            {
                "CPOSTAG": "ns",
                "DEPREL": "定中关系",
                "ID": 3,
                "LEMMA": "北京",
                "NAME": "未##地",
                "POSTAG": "ns",
                "HEAD": 4
            },
            {
                "CPOSTAG": "ns",
                "DEPREL": "动宾关系",
                "ID": 4,
                "LEMMA": "天安门",
                "NAME": "未##地",
                "POSTAG": "ns",
                "HEAD": 2
            }
        ]
        self.assertEqual(len(ret), len(sample_output))
        for r, s in zip(ret, sample_output):
            self.assertEqual(r['ID'], s['ID'])
            self.assertEqual(r['DEPREL'], s['DEPREL'])


if __name__ == '__main__':
    unittest.main()
