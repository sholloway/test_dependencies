# https://en.wikipedia.org/wiki/Base62
# https://normaltool.com/dencoders/base62-encoder
class Base62:
  ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  ALPHABET_LEN = 62 

  def encode(self, number: int) -> str:
    'Encode a positive number in Base62.'
    encoded_characters: list[str] = []
    if number == 0:
      return '0'
    
    while number:
      number, remainder = divmod(number, Base62.ALPHABET_LEN)
      encoded_characters.append(Base62.ALPHABET[remainder])

    encoded_characters.reverse()
    return ''.join(encoded_characters)

  def decode(self, encoded: str) -> int:
    """Decodes a base62 string into a positive number."""
    encoded_len = len(encoded)
    decoded_number = 0

    position: int = 0
    for token in encoded:
      power = encoded_len - (position + 1)
      decoded_number += Base62.ALPHABET.index(token) * (Base62.ALPHABET_LEN ** power)
      position += 1
    return decoded_number