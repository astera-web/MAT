"""Численная проверка гипотез Гольдбаха и Коллатца.

Это НЕ доказательство: проверка конечного диапазона ничего не говорит
о всех числах. Скрипт лишь ищет контрпримеры.
"""
import sys


def sieve(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i :: i] = bytearray(len(range(i * i, n + 1, i)))
    return s


def goldbach(limit):
    """Для каждого чётного 4 <= n <= limit ищет простые p + q = n."""
    s = sieve(limit)
    primes = [i for i in range(2, limit + 1) if s[i]]
    for n in range(4, limit + 1, 2):
        for p in primes:
            if p > n // 2:
                return n  # контрпример
            if s[n - p]:
                break
    return None


def collatz(limit):
    """Проверяет, что все n <= limit доходят до 1 (с кэшем)."""
    cache = {1: 0}
    best = (1, 0)
    for n in range(2, limit + 1):
        x, path = n, []
        while x not in cache:
            path.append(x)
            x = x // 2 if x % 2 == 0 else 3 * x + 1
        steps = cache[x]
        for v in reversed(path):
            steps += 1
            if v <= limit:
                cache[v] = steps
        if cache[n] > best[1]:
            best = (n, cache[n])
    return best


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    c = goldbach(N)
    print(f"Гольдбах до {N}:", "контрпример " + str(c) if c else "контрпримеров нет")
    n, st = collatz(N)
    print(f"Коллатц до {N}: все дошли до 1; самый долгий путь n={n}, шагов={st}")
