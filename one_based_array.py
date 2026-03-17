"""IPA擬似言語の1-based配列

擬似言語の配列は添字が1から始まる。このモジュールは1-basedの配列クラスを提供する。
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, overload


class Array:
    """IPA擬似言語の1-based配列

    擬似言語の配列は添字が1から始まる。Pythonの0-basedリストとの変換を内部で行う。

    Examples:
        >>> arr = Array(5)
        >>> arr[1] = 10
        >>> arr[1]
        10
        >>> arr = Array.from_literal([11, 12, 13, 14, 15])
        >>> arr[4]
        14
        >>> len(arr)
        5
    """

    def __init__(self, size: int = 0, init: Any = None) -> None:
        """配列を生成する

        Args:
            size: 配列の要素数
            init: 初期値（デフォルトはNone=未定義）
        """
        self._data: list[Any] = [init] * size
        self._size: int = size

    @classmethod
    def from_literal(cls, values: list[Any]) -> Array:
        """リテラル値のリストから配列を生成する

        Args:
            values: 要素のリスト（例: [11, 12, 13]）

        Returns:
            生成された Array
        """
        arr = cls(len(values))
        arr._data = list(values)
        return arr

    def __getitem__(self, index: int) -> Any:
        self._validate_index(index)
        return self._data[index - 1]

    def __setitem__(self, index: int, value: Any) -> None:
        self._validate_index(index)
        self._data[index - 1] = value

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"Array({self._data})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Array):
            return self._data == other._data
        return NotImplemented

    def append(self, value: Any) -> None:
        """末尾に値を追加する"""
        self._data.append(value)
        self._size += 1

    def to_list(self) -> list[Any]:
        """Python標準のリストとして返す"""
        return list(self._data)

    def _validate_index(self, index: int) -> None:
        if not (1 <= index <= self._size):
            raise IndexError(
                f"添字が範囲外です: {index}（有効範囲: 1〜{self._size}）"
            )


class Array2D:
    """IPA擬似言語の1-based二次元配列

    二次元配列の要素番号は、行番号、列番号の順に","で区切って指定する。

    Examples:
        >>> arr = Array2D(2, 3, init=0)
        >>> arr[1, 2] = 42
        >>> arr[1, 2]
        42
        >>> arr = Array2D.from_literal([[11, 12, 13], [21, 22, 23]])
        >>> arr[2, 3]
        23
    """

    def __init__(self, rows: int, cols: int, init: Any = None) -> None:
        """二次元配列を生成する

        Args:
            rows: 行数
            cols: 列数
            init: 初期値（デフォルトはNone=未定義）
        """
        self._data: list[list[Any]] = [[init] * cols for _ in range(rows)]
        self._rows: int = rows
        self._cols: int = cols

    @classmethod
    def from_literal(cls, values: list[list[Any]]) -> Array2D:
        """リテラル値の二次元リストから配列を生成する

        Args:
            values: 二次元リスト（例: [[11, 12], [21, 22]]）

        Returns:
            生成された Array2D
        """
        if not values:
            return cls(0, 0)
        rows = len(values)
        cols = len(values[0])
        arr = cls(rows, cols)
        arr._data = [list(row) for row in values]
        return arr

    @overload
    def __getitem__(self, index: tuple[int, int]) -> Any: ...

    @overload
    def __getitem__(self, index: int) -> list[Any]: ...

    def __getitem__(self, index: tuple[int, int] | int) -> Any:
        if isinstance(index, tuple):
            r, c = index
            self._validate_index(r, c)
            return self._data[r - 1][c - 1]
        # 行のみ指定: 1-basedで行全体を返す
        self._validate_row(index)
        return self._data[index - 1]

    def __setitem__(self, index: tuple[int, int], value: Any) -> None:
        if not isinstance(index, tuple):
            raise TypeError("二次元配列の代入には (行, 列) のタプルが必要です")
        r, c = index
        self._validate_index(r, c)
        self._data[r - 1][c - 1] = value

    @property
    def rows(self) -> int:
        """行数"""
        return self._rows

    @property
    def cols(self) -> int:
        """列数"""
        return self._cols

    def row(self, r: int) -> list[Any]:
        """指定行（1-based）の全要素を返す"""
        self._validate_row(r)
        return list(self._data[r - 1])

    def col(self, c: int) -> list[Any]:
        """指定列（1-based）の全要素を返す"""
        self._validate_col(c)
        return [self._data[r][c - 1] for r in range(self._rows)]

    def __repr__(self) -> str:
        return f"Array2D({self._data})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Array2D):
            return self._data == other._data
        return NotImplemented

    def _validate_index(self, r: int, c: int) -> None:
        if not (1 <= r <= self._rows):
            raise IndexError(
                f"行番号が範囲外です: {r}（有効範囲: 1〜{self._rows}）"
            )
        if not (1 <= c <= self._cols):
            raise IndexError(
                f"列番号が範囲外です: {c}（有効範囲: 1〜{self._cols}）"
            )

    def _validate_row(self, r: int) -> None:
        if not (1 <= r <= self._rows):
            raise IndexError(
                f"行番号が範囲外です: {r}（有効範囲: 1〜{self._rows}）"
            )

    def _validate_col(self, c: int) -> None:
        if not (1 <= c <= self._cols):
            raise IndexError(
                f"列番号が範囲外です: {c}（有効範囲: 1〜{self._cols}）"
            )
