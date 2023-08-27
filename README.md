# DecodED Python3 Chess


Thanks to Liudmil Mitev, wyojustin, and sohrabtowfighi for the base repository.
https://github.com/sohrabtowfighi/Simple-Python3-Chess

```py
class Board:
    # ...
    def _get_rows(self, fen: str):
        return fen.split("/")

    def _is_cell_empty(self, val: str) -> bool:
        return val == " "
```