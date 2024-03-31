from test_dependencies.base62 import Base62

class TestBase62Encoding:
  def test_encoding(self) -> None:
    base62 = Base62()
    assert base62.encode(0) == '0'
    assert base62.encode(5) == '5'
    assert base62.encode(13) == 'd'
    assert base62.encode(47) == 'L'
    assert base62.encode(57) == 'V'
    assert base62.encode(100) == '1C'
    assert base62.encode(123456789089898) == 'z3wBXxG2'

  def test_decoding(self) -> None:
    base62 = Base62()
    assert base62.decode('0') == 0
    assert base62.decode('5') == 5
    assert base62.decode('d') == 13
    assert base62.decode('L') == 47
    assert base62.decode('V') == 57
    assert base62.decode('1C') == 100
    assert base62.decode('z3wBXxG2') == 123456789089898