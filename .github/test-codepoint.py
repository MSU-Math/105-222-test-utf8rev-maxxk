from libtester import prepare, SR
import collections
import difflib
import itertools
import functools
import logging
import math
import operator
import os
import random
import sys
import textwrap
import traceback

def pairs(iterable):
    a, b = itertools.tee(iterable)
    odd = itertools.islice(a, 0, None, 2)
    even = itertools.islice(itertools.chain(b, [""]), 1, None, 2)
    return zip(odd, even)

def main():
    e = prepare()
    if not e:
        print("Программа не скомпилирована")
        sys.exit(1)

    os.environ["ASAN_OPTIONS"] = "exitcode=154"

    errors = 0

    def testcase(value):
        if isinstance(value, str):
            value = value.encode('utf-8')
        result = e.expect_success(value[:10], input=value)
        if not result:
            return result
        
        try:
            filtered = ""
            start = 0
            while True:
                try:
                    filtered += value[start:].decode('utf-8')
                    break
                except UnicodeError as ex:
                    if ex.start > 0:
                        filtered += ex.object[:ex.start].decode('utf-8')
                    start += ex.start + 1
            answer = "".join(b + a for a, b in pairs(filtered))
            if answer != result.stdout:
                print(SR)
                print("ОШИБКА: ответ не совпадает с ожидаемым.")
                print("Первые несколько отличий (A - правильный ответ, B - ошибочный ответ):")
                difference = difflib.SequenceMatcher(None, answer, result.stdout)
                for tag, i1, i2, j1, j2 in itertools.islice((o for o in difference.get_opcodes() if o[0] != "equal"), 0, 5):
                    fragment_left = answer[i1:i1+min(i2-i1, 10)]
                    fragment_right = result.stdout[j1:j1+min(j2-j1, 10)]
                    print("{:7}  A[{}:{}] --> B[{}:{}]\t{!r:>8} --> {!r}".format(tag, i1, i2, j1, j2, fragment_left, fragment_right))
                return False
            else:
                return result
        except Exception:
            print(SR)
            print("ОШИБКА: Не удалось разобрать вывод программы")
            traceback.print_exc()
            return False

    errors += not testcase("abcdefghikjlmonpqrstuvwxyz выфащшуцфоа авфцу шкзыва ьсфзуцла ьцфдулаыфждвьаыф " * 10)
    errors += not testcase("Ы")
    errors += not testcase("АБ")
    errors += not testcase("АБВ")
    errors += not testcase("АБВГ")
    
    lipsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
    lipsum += "В чащах юга жил-был цитрус... — да, но фальшивый экземпляръ!"
    lipsum += "!$%^&*()_)(*&^%$#@)SDAFSHEfdsafaTWTwaefsVCDSgaewrfs   \n\r\n\n\n\ndf"
    lipsum += "∞«»>⩽≥αβγδεϟςρτυθιοπ[{}]σφγηξκλζχωωβνμ¡&&\"ꙮ≈—''"
    errors += not testcase(lipsum)
    errors += not testcase(lipsum * 10)
    errors += not testcase(lipsum * 100)
    lipsum = lipsum.encode('utf-8')
    errors += not testcase(b"\xc1" + lipsum)
    errors += not testcase(lipsum + b"\xd1")
    errors += not testcase(b"\xe1"+ lipsum)
    errors += not testcase(b"\xe1\x82"+ lipsum)
    errors += not testcase(lipsum + b"\xf1")
    errors += not testcase(b"\x81\x91\xa1\xb1\xf1" + lipsum)
    errors += not testcase(lipsum + b"\xf5"*50)
        
    print(f"Тестирование завершено, количество ошибок: {errors}")

    sys.exit(errors)

main()
