import unittest
import foodypy

class FoodyPyTestSuit(unittest.TestCase):
    def test_Nutrients_properties(self):
        n = foodypy.Nutrients(8, 7, 6, 5)
        self.assertEqual(n.fat, 8)
        self.assertEqual(n.carbs, 7)
        self.assertEqual(n.protein, 6)
        self.assertEqual(n.fiber, 5)
        self.assertEqual(n.calories, 9 * n.fat + 4 * n.carbs + 4 * n.protein)

    def test_Nutrients_errors(self):
        for nutrient in ['fat', 'carbs', 'protein', 'fiber']:
            with self.assertRaisesRegex(TypeError, rf"Expected '{nutrient}'"):
                foodypy.Nutrients(**{nutrient: 'bad'})

            with self.assertRaisesRegex(ValueError, rf"Expected '{nutrient} >= 0'"):
                foodypy.Nutrients(**{nutrient: -1})

    def test_Nutrients_add(self):
        test_cases = [
            # a, b, res_check
            (foodypy.Nutrients(), foodypy.Nutrients(), foodypy.Nutrients()),
            (
                foodypy.Nutrients(1, 2, 3, 4),
                foodypy.Nutrients(2, 4, 6, 8),
                foodypy.Nutrients(3, 6, 9, 12),
            ),
        ]

        for nutrient in ['fat', 'carbs', 'protein', 'fiber']:
            test_cases.append((
                foodypy.Nutrients(**{nutrient: 10}),
                foodypy.Nutrients(**{nutrient: 20}),
                foodypy.Nutrients(**{nutrient: 30}),
            ))

        for a, b, res_check in test_cases:
            res = a + b
            self.assertEqual(res, res_check)

    def test_Nutrients_sub(self):
        test_cases = [
            # a, b, res_check
            (foodypy.Nutrients(), foodypy.Nutrients(), foodypy.Nutrients()),
            (
                foodypy.Nutrients(3, 6, 9, 12),
                foodypy.Nutrients(1, 2, 3, 4),
                foodypy.Nutrients(2, 4, 6, 8),
            ),
        ]

        for nutrient in ['fat', 'carbs', 'protein', 'fiber']:
            test_cases.append((
                foodypy.Nutrients(**{nutrient: 30}),
                foodypy.Nutrients(**{nutrient: 10}),
                foodypy.Nutrients(**{nutrient: 20}),
            ))

        for a, b, res_check in test_cases:
            res = a - b
            self.assertEqual(res, res_check)

    def test_Nutrients_mul(self):
        test_cases = [
            # a, b, res_check
            (foodypy.Nutrients(), foodypy.Nutrients(), foodypy.Nutrients()),
            (
                foodypy.Nutrients(1, 2, 3, 4),
                foodypy.Nutrients(2, 4, 6, 8),
                foodypy.Nutrients(2, 8, 18, 32),
            ),
            (
                foodypy.Nutrients(1, 2, 3, 4),
                3,
                foodypy.Nutrients(3, 6, 9, 12),
            ),
            (
                3,
                foodypy.Nutrients(1, 2, 3, 4),
                foodypy.Nutrients(3, 6, 9, 12),
            ),
        ]

        for nutrient in ['fat', 'carbs', 'protein', 'fiber']:
            test_cases.append((
                foodypy.Nutrients(**{nutrient: 10}),
                foodypy.Nutrients(**{nutrient: 20}),
                foodypy.Nutrients(**{nutrient: 200}),
            ))

            test_cases.append((
                foodypy.Nutrients(**{nutrient: 10}),
                0.3,
                foodypy.Nutrients(**{nutrient: 3}),
            ))

            test_cases.append((
                10,
                foodypy.Nutrients(**{nutrient: 0.3}),
                foodypy.Nutrients(**{nutrient: 3}),
            ))

        for a, b, res_check in test_cases:
            res = a * b
            self.assertEqual(res, res_check)

    def test_Nutrients_div(self):
        test_cases = [
            # a, b, res_check
            (foodypy.Nutrients(), foodypy.Nutrients(1, 1, 1, 1), foodypy.Nutrients()),
            (
                foodypy.Nutrients(2, 8, 18, 32),
                foodypy.Nutrients(2, 4, 6, 8),
                foodypy.Nutrients(1, 2, 3, 4),
            ),
            (
                foodypy.Nutrients(3, 6, 9, 12),
                3,
                foodypy.Nutrients(1, 2, 3, 4),
            ),
        ]

        for nutrient in ['fat', 'carbs', 'protein', 'fiber']:
            ones = foodypy.Nutrients(1, 1, 1, 1)
            test_cases.append((
                foodypy.Nutrients(**{nutrient: 200}),
                foodypy.Nutrients(**{nutrient: 9}) + ones,
                foodypy.Nutrients(**{nutrient: 20}),
            ))

            test_cases.append((
                foodypy.Nutrients(**{nutrient: 3}),
                0.3,
                foodypy.Nutrients(**{nutrient: 10}),
            ))

        for a, b, res_check in test_cases:
            res = a / b
            self.assertEqual(res, res_check)

if __name__ == '__main__':
    unittest.main()
