import pytest

from test_dependencies.id_generator import IDGenerationError, IDGenerator 

class TestIdGenerator:
  def test_invalid_d_parameters(self) -> None:
    gen = IDGenerator()
    with pytest.raises(IDGenerationError) as e:
      gen.next_id(prefix='abcd')
    assert str(e.value) == 'The ID prefix must be exactly 3 characters. A prefix of length 4 was provided.'
    
    with pytest.raises(IDGenerationError) as e:
      gen.next_id(host='abcde')
    assert str(e.value) == 'The ID host must be exactly 2 characters. A host of length 5 was provided.'
    
    with pytest.raises(IDGenerationError) as e:
      gen.next_id(checksum='a')
    assert str(e.value) == 'The ID checksum must be exactly 3 characters. A checksum of length 1 was provided.'

  def test_id_length(self) -> None:
    gen = IDGenerator()
    assert len(gen.next_id()) == 18

  def test_id_format(self) -> None:
    low_id_generator = IDGenerator()
    assert low_id_generator.next_id() == '01p0M0000000001QAY'
    assert low_id_generator.next_id() == '01p0M0000000002QAY'
    assert low_id_generator.next_id() == '01p0M0000000003QAY'
    assert low_id_generator.next_id() == '01p0M0000000004QAY'
    assert low_id_generator.next_id() == '01p0M0000000005QAY'

    high_id_generator = IDGenerator(starting_id=12_345_678_910)
    assert high_id_generator.next_id() == '01p0M0000dtvd3pQAY'
    assert high_id_generator.next_id() == '01p0M0000dtvd3qQAY'
    assert high_id_generator.next_id() == '01p0M0000dtvd3rQAY'