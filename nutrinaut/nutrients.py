class Nutrients:
    '''Holds nutrition data. Supports some array arithmetic operations.
    '''
    def __init__(self, fat=0, carbs=0, protein=0):
        self._fat = fat
        self._carbs = carbs
        self._protein = protein

    @property
    def fat(self):
        return self._fat

    @property
    def carbs(self):
        return self._carbs

    @property
    def protein(self):
        return self._protein

    @property
    def calories(self):
        return (9 * self.fat) + (4 * self.carbs) + (4 * self.protein)

    def __str__(self):
        return f'Nutrients(fat={self.fat}, carbs={self.carbs}, protein={self.protein}, calories={self.calories})'

    def __repr__(self):
        return str(self)

    def _binary_op(self, other, op):
        if isinstance(other, Nutrients):
            return Nutrients(
                fat=op(self.fat, other.fat),
                carbs=op(self.carbs, other.carbs),
                protein=op(self.protein, other.protein))
        else:
            return Nutrients(
                fat=op(self.fat, other),
                carbs=op(self.carbs, other),
                protein=op(self.protein, other))

    def __add__(self, other):
        return self._binary_op(other, lambda a, b: a + b)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self._binary_op(other, lambda a, b: a - b)

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        return self._binary_op(other, lambda a, b: a * b)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self._binary_op(other, lambda a, b: a / b)

def macros(fat=0, carbs=0, protein=0):
    '''Creates a :class:`Nutrients` object from macronutrients.
    '''
    return Nutrients(fat=fat, carbs=carbs, protein=protein)
