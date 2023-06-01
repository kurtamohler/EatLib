class Nutrients:
    '''
    Holds nutrition data. Supports basic array arithmetic operations.

    .. note::

       This currently only tracks fat, carbohydrate, protein, and fiber
       amounts.  Calories are estimated based on fat, carbs, and protein.
    '''
    def __init__(self, fat=0, carbs=0, protein=0, fiber=0):
        '''
        Args:

          fat (number, optional):
            Total fat, in grams

            Default: 0

          carbs (number, optional):
            Total carbohydrates, in grams

            Default: 0

          protein (number, optional):
            Total protein, in grams

            Default: 0

          fiber (number, optional):
            Total fiber, in grams

            Default: 0
        '''
        self._fat = fat
        self._carbs = carbs
        self._protein = protein
        self._fiber = fiber

    @property
    def fat(self):
        '''
        Total fat, in grams

        Returns:
          number:
        '''
        return self._fat

    @property
    def carbs(self):
        '''
        Total carbohydrates, in grams

        Returns:
          number:
        '''
        return self._carbs

    @property
    def protein(self):
        '''
        Total protein, in grams

        Returns:
          number:
        '''
        return self._protein

    @property
    def fiber(self):
        '''
        Total fiber, in grams

        Returns:
          number:
        '''
        return self._fiber

    @property
    def calories(self):
        '''
        Total energy, in Calories (kilocalories or kcal). Note that "Calories",
        with a capital "C", often seen on Nutrition Facts labels,
        conventionally refers to kilocalories.

        This value is estimated based on the heuristic that one gram of
        :attr:`fat`, :attr:`carbs`, and :attr:`protein` contain 9 kcal,
        4 kcal, and 4 kcal, respectively.

        Returns:
          number:
        '''
        return (9 * self.fat) + (4 * self.carbs) + (4 * self.protein)

    def __str__(self):
        return f'Nutrients(fat={self.fat}, carbs={self.carbs}, protein={self.protein}, calories={self.calories}, fiber={self.fiber})'

    def __repr__(self):
        return str(self)

    def _binary_op(self, other, op):
        if isinstance(other, Nutrients):
            return Nutrients(
                fat=op(self.fat, other.fat),
                carbs=op(self.carbs, other.carbs),
                protein=op(self.protein, other.protein),
                fiber=op(self.fiber, other.fiber))
        else:
            return Nutrients(
                fat=op(self.fat, other),
                carbs=op(self.carbs, other),
                protein=op(self.protein, other),
                fiber=op(self.fiber, other))

    def __add__(self, other):
        '''
        Add ``other`` element-wise.

        Args:
          other (number or :class:`Nutrients`):
            Amount to add
        Returns:
          :class:`foodypy.Nutrients`:
        '''
        return self._binary_op(other, lambda a, b: a + b)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        '''
        Subtract by ``other`` element-wise.

        Args:
          other (number or :class:`Nutrients`):
            Amount to subtract
        Returns:
          :class:`foodypy.Nutrients`:
        '''
        return self._binary_op(other, lambda a, b: a - b)

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        '''
        Multiply by ``other`` element-wise.

        Args:
          other (number or :class:`Nutrients`):
            Amount to multipy by
        Returns:
          :class:`foodypy.Nutrients`:
        '''
        return self._binary_op(other, lambda a, b: a * b)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        '''
        Divide by ``other`` element-wise.

        Args:
          other (number or :class:`Nutrients`):
            Amount to divide by
        Returns:
          :class:`foodypy.Nutrients`:
        '''
        return self._binary_op(other, lambda a, b: a / b)
