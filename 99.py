import numpy as np
from tabulate import tabulate


class Solver:
    def __init__(self, function, interval, delta=1e-6, eps=1e-6, n=25):
        self.function = function
        self.a, self.b = min(interval), max(interval)
        self.delta = delta
        self.eps = eps
        self.n = n

    def solve(self, method, return_borders=False):
        _method_ = self._get_method(method)
        return _method_(return_borders)

    def _get_method(self, method):
        """Возвращает функцию метода в зависимости от переданного строкового параметра method."""
        method_dict = {"dichotomy": self._dichotomy, "golden_ratio": self._golden_ratio, "fibonacci": self._fibonacci,
                       "random_search": self._random_search}
        return method_dict.get(method)

    def _dichotomy(self, return_borders):
        """Метод дихотомии или деления отрезков пополам."""
        a_s = [self.a, ]
        b_s = [self.b, ]
        while b_s[-1]-a_s[-1] > 2 * self.eps:
            l_s = (a_s[-1]+b_s[-1]-self.delta) / 2
            r_s = (a_s[-1]+b_s[-1]+self.delta) / 2
            if self.function(l_s) > self.function(r_s):
                a_s.append(l_s)
                b_s.append(b_s[-1])
            elif self.function(l_s) < self.function(r_s):
                a_s.append(a_s[-1])
                b_s.append(r_s)
            else:
                a_s.append(l_s)
                b_s.append(r_s)
        x = (b_s[-1] + a_s[-1]) / 2
        y = self.function(x)
        if return_borders:
            borders = tabulate(np.array((a_s, b_s)).T, headers=['a', 'b'], showindex="always", tablefmt="github")
        else:
            borders = None
        return x, y, borders

    def _golden_ratio(self, return_borders):
        """Метод золотого сечения."""
        a_s = [self.a, ]
        b_s = [self.b, ]
        tau = (np.sqrt(5) - 1) / 2
        while b_s[-1]-a_s[-1] > self.eps:
            l_s = b_s[-1] - tau * (b_s[-1] - a_s[-1])
            r_s = a_s[-1] + tau * (b_s[-1] - a_s[-1])
            if self.function(l_s) > self.function(r_s):
                a_s.append(l_s)
                b_s.append(b_s[-1])
            else:
                a_s.append(a_s[-1])
                b_s.append(r_s)
        x = (b_s[-1] + a_s[-1]) / 2
        y = self.function(x)
        if return_borders:
            borders = tabulate(np.array((a_s, b_s)).T, headers=['a', 'b'], showindex="always", tablefmt="github")
        else:
            borders = None
        return x, y, borders

    def _fibonacci(self, return_borders):
        """Метод Фибоначчи."""
        a_s = [self.a, ]
        b_s = [self.b, ]
        fibonacci_numbers = self._fibonacci_sequence()
        for s in np.arange(self.n-1):
            if s < self.n-2:
                tau = fibonacci_numbers[self.n-s-1] / fibonacci_numbers[self.n-s]
            else:
                tau = (1+self.delta) / 2
            l_s = b_s[-1] - tau * (b_s[-1] - a_s[-1])
            r_s = a_s[-1] + tau * (b_s[-1] - a_s[-1])
            if self.function(l_s) > self.function(r_s):
                a_s.append(l_s)
                b_s.append(b_s[-1])
            elif self.function(l_s) < self.function(r_s):
                a_s.append(a_s[-1])
                b_s.append(r_s)
            else:
                a_s.append(l_s)
                b_s.append(r_s)
        x = (b_s[-1] + a_s[-1]) / 2
        y = self.function(x)
        if return_borders:
            borders = tabulate(np.array((a_s, b_s)).T, headers=['a', 'b'], showindex="always", tablefmt="github")
        else:
            borders = None
        return x, y, borders

    def _fibonacci_sequence(self):
        fibonacci_sequence = [1, ]
        if self.n == 1:
            fibonacci_sequence.append(1)
        elif self.n != 0:
            while len(fibonacci_sequence) <= self.n:
                fibonacci_sequence.append(sum(fibonacci_sequence[-2:]))
        return fibonacci_sequence

    def _random_search(self, return_numbers):
        """Метод случайного поиска."""
        samples_x = np.random.uniform(self.a, self.b, size=self.n)
        samples_y = tuple(self.function(x) for x in samples_x)
        index = np.argmin(samples_y)
        x = samples_x[index]
        y = samples_y[index]
        if return_numbers:
            numbers = tabulate(np.array((samples_x, samples_y)).T, headers=['x', 'y'], showindex="always",
                               tablefmt="github")
        else:
            numbers = None
        return x, y, numbers


if __name__ == '__main__':
    _exit_ = False
    while not _exit_:
        a_input = float(input("Введіть ліву межу інтервалу: "))
        b_input = float(input("Введіть праву межу інтервалу: "))
        if a_input > b_input:
            raise Exception("Ліва межа не може перевищувати праву!")
        interval_input = [a_input, b_input]
        method_input = input("Введіть метод зі списку: dichotomy, golden_ratio, fibonacci, random_search\n")
        if method_input not in {"dichotomy", "golden_ratio", "fibonacci", "random_search"}:
            raise Exception("Хибна назва методу!")
        is_min = input("Функція мінімізується? Так/Ні: ")
        if is_min == "Так":
            is_min = True
        elif is_min == "Ні":
            is_min = False
        else:
            raise Exception("Нерозпізнана опція щодо мінімізації чи максимізації!")
        return_borders = input("Чи потрібно виводити кроки пошуку межі? Так/Ні: ")
        if return_borders == "Так":
            return_borders = True
        elif return_borders == "Ні":
            return_borders = False
        else:
            raise Exception("Нерозпізнана опція щодо кроків пошуку межі!")


        function = lambda x: np.exp(-x) - 2*np.cos(x)


        if not is_min:
            y_mod = -1
        else:
            y_mod = 1
        x, y, table = Solver(lambda x: y_mod*function(x), interval_input).solve(method_input, return_borders)
        if return_borders:
            print(table)
        print(f"x: {x}; y: {y*y_mod}")
        ex = input("Бажаєте вийти з програми? Так/Ні: ")
        if ex == "Так":
            ex = True
        elif ex == "Ні":
            ex = False
        else:
            raise Exception("Нерозпізнана опція щодо виходу з програми!")