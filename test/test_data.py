import io
import os

import pytest

from data import numberer, reader, token


def test_token():
    with pytest.raises(TypeError):
        token.Token()
    t = token.Token("Test")
    assert t.form == "Test"
    assert t.lemma is None and t.misc is None
    t2 = token.Token("Test")
    assert t == t2


def test_token_str():
    t = token.Token("Test")
    assert str(t) == "Test\t_\t_\t_\t_\t_\t_\t_\t_"
    t = token.Token("Test", lemma="test")
    assert str(t) == "Test\ttest\t_\t_\t_\t_\t_\t_\t_"
    t = token.Token("Test", lemma="test", misc="misc")
    assert str(t) == "Test\ttest\t_\t_\t_\t_\t_\t_\tmisc"


def test_reader_single(tests_root):
    path = os.path.join(tests_root, "data", "single.conllu")
    r = reader.read_sentences(path)
    sent = next(r)
    with pytest.raises(StopIteration):
        next(r)
    assert len(sent) == 4
    t1 = token.Token("This", "T", misc="Something in misc")
    t2 = token.Token("is", "E")
    t3 = token.Token("a", "S")
    t4 = token.Token("Test", "T")
    target = [t1, t2, t3, t4]
    assert sent == target


def test_reader(tests_root):
    path = os.path.join(tests_root, "data", "test.conllu") #TODO changed from single.conllu to test.conllu
    r = reader.read_sentences(path)
    assert not isinstance(r, list)
    test_sentences = [sent for sent in r]
    assert len(test_sentences) == 4

    # simple example sentence
    first = test_sentences[0]
    assert len(first) == 5
    assert first[0] == token.Token("Veruntreute", "veruntreuen")
    assert str(first[0]) == "Veruntreute\tveruntreuen\t_\t_\t_\t_\t_\t_\t_"
    assert first[-1] == token.Token("?", "?")

    # sentence with multi-word in beginning
    second = test_sentences[1]
    assert len(second) == 4
    assert second[0] == token.Token("This", "T")
    assert second[-1] == token.Token("Test", "T")

    # sentence with multiple preceeding blanks
    third = test_sentences[2]
    assert len(third) == 4
    assert third[0] == token.Token("This", "T")
    assert third[-1] == token.Token("Test", "T")

    # sentence with space in form field
    last = test_sentences[3]
    assert len(last) == 3
    assert last[0] == token.Token("Another", "another")
    assert last[-1] == token.Token("with spaces", "T")


def test_numberer():
    n = numberer.Numberer()
    assert len(n) == 1
    assert n.value2idx("<UNK>", False) == 0
    assert n.value2idx("<UNK>", True) == 0
    assert n.value2idx("definitely not in vocab", False) == 0
    assert n.value2idx("definitely not in vocab", True) == 1
    assert n.value2idx("definitely not in vocab", True) == 1

    seq = ["a", "c", "b", "c"]
    assert list(n.seq2indices(seq, False)) == 4*[0]
    assert list(n.seq2indices(seq, True)) == [2, 3, 4, 3]
    assert list(n.indices2seq([2, 3, 4, 3])) == ["a", "c", "b", "c"]

    indices = range(5)
    assert list(n.indices2seq(indices)) == ["<UNK>", "definitely not in vocab", "a", "c", "b"]

    mem_file = io.StringIO()
    n.save(mem_file)
    mem_file.seek(0)
    n2 = numberer.Numberer.load(mem_file)
    target_vals = list(n.indices2seq(range(0, len(n))))
    assert target_vals == list(n2.indices2seq(range(0, len(n2))))
    assert list(n.seq2indices(target_vals, False)) == list(n2.seq2indices(target_vals, False))
