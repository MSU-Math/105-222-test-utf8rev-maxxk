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
import grapheme

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
            answer = "".join(b + a for a, b in pairs(grapheme.graphemes(filtered)))
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

    errors += not testcase("abcdefghikjlmonpqrstuvwxyz выфащшуцфоа авфцу шкзыва ьсфзуцла ьцфдулаыфждвьаыф 🏴‍☠️🏴🇦🇩🇷🇺🇷 🇺🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣 󠁴󠁿" * 10)
    errors += not testcase("🌈")
    errors += not testcase("🌈🌞")
    errors += not testcase("🏴󠁧󠁢󠁳󠁣󠁴󠁿🏴‍☠️")
    errors += not testcase("🏴‍☠️🏴󠁧󠁢󠁳󠁣󠁴󠁿🏴‍☠️")
    
    lipsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
    lipsum += "В чащах юга жил-был цитрус... — да, но фальшивый экземпляръ!"
    lipsum += "!$%^&*()_)(*&^%$#@)SDAFSHEfdsafaTWTwaefsVCDSgaewrfs   \n\r\n\n\n\ndf"
    lipsum += "∞«»>⩽≥αβγδεϟςρτυθιοπ[{}]σφγηξκλζχωωβνμ¡&&\"ꙮ≈—''"
    lipsum += "🏴‍☠️🏴🇦🇩🇷🇺🇷 🇺🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁳󠁣 󠁴" * 30
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
    errors += not testcase("ȧ̬͉̻̭̒̒͊b͙̖̭̫̫̫͓̭̣̆̈́͐̎̑́̀̓̒cd̻͛e̝̯̞͚ͪ̐̅ͤf͙͚̣̲͔͕̯͓͓̻͚̐̈̋̏ͭ̐̊ͤ͆̾̌g͕̝̬̝͕͙̹̱̠͔͂̓ͩ̿ͦ͐ͩ͊̒͌͌ͅh̳͉i͓̠͓̭̻̠̪̠̖̰̤͍j̠͉̱̻̯̫͒̒̎̈́̒ͦkl͇̹̦̮̮m̞͍̰̺͖̈́̓̃̽ͯn͍̩̱͓̺͈͑̓̄̆̃̆o̭pa̐b̗̖͎͛́͗c̘̠̙̓́͂d͉̘͉̬͈̬ef̺̣̫̞͙̼g̓͆̌ͧ̅̊̂̂̂͑͋h̿ͯͫ̔ͫ̏̓̚i͖̦j̟͓̗̝̩̤͔̰̣̣͈̼̥͈̫̅̒͌̇̍ͣͣͦͫ̎̇̂ͭ̋̿k̯̪̬̟̻̙̙͙̤l͒ͭ̒̄́ͧ͗̆̏mnͮͥͤͮ̈́ͧop͈̓a̙͓̮͕̬̺̝b͉̯̰̪̂ͯͯ̉͌ͅc̜̬͎͚ͩ͌ͨ̽dẽ̮̟̮̳͍̺̜̯̺͈̭̤͚̋ͦ̓͗ͨ̅̓͆͒ͭ̐͗fg̝̹̻̼̭̹̻̺h̬͈͖̤͉̰ͪ̐̊ͯ̀̏î̗͍͙͙̫͍͍̟̮̰̩̺͈̩̟̍ͤ͂̾̋̽ͮ̃ͨ̌̎̽̉̚j͔͈̦̙̖͖͚̜͉̹̲̆̽̎̿ͬ̓̈̈̏ͭͨ̂ͅk̲̗̼̦͍̘l͔̟̹̥͉̠͎͔̲m̪̖̱̤̼̼̙̈̑̓̂̂̈̈́no̰̗̤̥͈̺͓͙̞̥͓̘̣͉ͣ͗͌͒͛̉ͨͨ̉̎ͯͬ͊ͣp̝͒ā͚̹̭̩̜̎̽͒ͤbc̤͙͈̱̲̳̻̓͂ͯ̂ͫͨ̾̚ͅdë͙̻̳̓̏f̖g̀hͬ̓͐̋̈̇̾̒̐ͣ̌͌i̙͓̘͓̖̬͖̠̞̱̮͎̔͑͐̌̉͒̈͐̓̇̈ͣ̔ͅj͎̭̭̫̹̹̳̹̗̘͐̔̈͌̿̽̏ͦ̓ͧk͈̮̅̐l̑ͫ̂ͣ͊̃mṇ͇̥̮̤͖̻̳͕̗̞ͧ̄ͦ̒͛̀̿͂ͯ̽̚op̗͓͔͍̰ͧͫͮ̾̈ab̘̤̥̠͙c̝͂d̖̟̰̤ͭ̏ͪ͗e̟̠͖̯̲̩̝͚f͈̺̂ͬgͫ̿͗̍̎̑̀ͩ̊ͪ̈́h̘͕̮̪͎̪̱̩͕͍̜̱̺̣̥i͎̣͍̪j̬͙k̭̰̹͙̙̝̥̖l̤̪̘̘̤̫̬̼̞͓͉ͧ̍̃͛ͤͫ͊̃͆͂̽ͥͅm̠̪̜̟̮̹̭̤n̝̥͇̱͎̬o̙̗̺̪̬̱̼͕p͚͙͙̤̱̺͔͍̗͓͍̒͌̽̓̌̄́͊̎̌͑ă̠b̩̗͎̮̦̺̙͍̖͍͕̅ͯ̆̃̌̔̌͋̄͛ͫcd̙̭̞͚͇̙̩̹͇̙̘͈̭̙ḛ̪̝̭̤fͩ̀̏͐͊̈́̑͐g͚̤͕̱ͩͯ̽̈ȟ͚̙̟̅ͤi̞j̦̣͖͚̿ͭ͐̂̚ͅk͖̜̓͛lm̖͎̯̘͕̭̤͊̅ͤ͊̓̀͋n̬̳̙̙͙̬̳õ̌̉̔̋̓̈ͭͯ̇p̖ͧả̏̒ͨ̽͌b̂ͨc̩̜̱̖̯̓͌̿̋̔d̉ͣͮè̯͙̗̺̹̪͎͎͖͇̤͇̝͉̾ͪ͆̐ͪ̎̓̿̓ͣ̽̃̈f̩̙̣̭̙̹̘͇̫ͨ̒ͦ̾͑̃͑ͥ̆g͉̘̻̭͕͙ͅhi͆̓̈̏ͩͭ̎̒̔̉̊j͚͓̞̰͈̠͙͚̬̳̻̩k̋̐̀l͈͉̜̗̣ṁ̜̬̠̩͔̥̖̘̤͕̝̝͈̮̫ͥ̇̇̂ͪͦ̀ͯ̅̈́ͤ̀̈́̈nͭ͌̂̽̓̽͋̓͗̑́ͯͨô̤̮̱͖͍̹̱̠̻̪̭̓ͦ̔ͤ͌ͬ̾ͭ͌̈́pͪ́̀ͣ̑a͈̝͚̯͕̥̹̭̿ͮ͋̒͋͋̔͌b͙̄c̆̒̎̔̿̂̽ͬͮ͒ͦ̎d̞̟̭̫͖̰̰̫͔̬̦̬ͯ͆̓ͩ͆̀ͬ̍ͧ́̾ͯ̉ͅeͧͨ̍ͧ̎̍͑͑ͨf͑̾̆ͫͪ̽̑ͯ̍̅͋ͩ̊̐̏g͐hȋ̎̑j͚̥͍̼͕̮͇͎̭̣̱̤̬̳͎ͤ̊̊́̓͐͊̐͋͌̿ͭͪ̾̈́k͚͔̘ͥ̏́l̟̼̼̦̼̳͉̪̦̣̮͙͍ͅmͩͪ͒̉̀̚̚n͙̟̻̙̫̼͗̓ͫ̇ͯ͋o̫̪̻̜̤͎̺̮̻͔̩̦̜͔̔͑̔͒̈́ͦͮ̿̽̌̇̐̈́ͬp͕̝͍̳̣͚̯̦̞̼͇͎̦͙̺̈͆ͪ̅̋̆̋ͨ͆ͩͤ̉́ͯ̽a̲ͣbc͊̑̀̎͗dͬ̒̊e̖̘̙̝͓̜̪̭͔̥̬̦̬͕̰̽̂ͫͫ͊̓͋ͣ͌̆̊ͤ̍ͨ̚f̆̉g̿̄ͣ̅̾͌̄͑ͨͥ́̚h̟̝͇̣̼̜͍̟̱̝͎̬̃̍͗̀ͮ̓̄̿̔͋͒̏ĭ̎͆͗͋ͣ̑̽ͭͦ́͑̍ͥ̀j͍̥̤̼͙͍̩̖̩̼͚̞͓̳ͅk̦̮̲̗̤̭̮̔͛̎̀̾̋͂l̤̣͇̯̻͓̻̟͍͚̈͊ͪ̐̂̓̑̿͒͒ͫͅm̜̜̺̉̾ͧń̦ỏ̻̭̰̩̱̯̝͖̹̥͊ͤͫ̽͌ͨͬ̐̆̚ͅp͇̗̫a̹͙̪̳̰̲̭͓̱̼̤͓̭̗̭ͥ̂̇ͨͪ̓ͫ̅̒̉̓ͪͭ̾ͣb̔́ͧ̓̽̔c̤̩̺͉ͅd͍̪̖͎̳͇̩͕̬̬̥͓̪̫̿͂ͪͯ̔ͦ̈́̇ͤ̄̇ͫͤͮe͍̣͖̺̤̼̗͇̻̩͗ͩ͑̄͋̎̊̀̒͒fg̋͒ͬ̓̉ͪͦ͐̈͆̚h̺̟̱̮̘͇̲́ͤͦͤ̋ͩ͛̈ͅi̬̣j̣̤̝̺̫͔̞̻̹̹͕̙k̬͎̣̯͈̯̞l̠̜̞̳͈̘̼͕̼m͖̖̼̺͎͔̪͍̲̪ͦͦ͐̅̿ͥ̿ͥ̈̍n̰̠͕̠̞͔̪͔̳̤̲͈͚͋ͣͤ̓̍̑ͧ̾͌͋ͧͣ͐o͎̞̫̦ͥ̋̌̓̇ͅp̹̳ͤͬa͊ͩ̃̄̏͌͆̃b̠̱͚̩̪͎͉̺̱̠̝̥͇̘̽̏̇́ͦͥ̄̉ͮ̄̈́́͋̚c͛ͤͯ̄͐͂̓ͤ̅̎̍d͎̠̗͔̉̈̆̚e͕͙͉̙͎̲̱̬̣̘̲̞̔ͩ͑͊̉ͯ̈́̋̍͑ͥͬ̒ͅf̰̺̗̤̖̰̮̳̭̣͙̺͙̝̎̇ͬ͋ͭͧ̎͋ͯͧ̎̊̔̅gͥh̫͕͙̲̙ͯ͑ͬͪ̆ï̜͎̬̇͛j̐̋̉ͭ̐̉k͇̩̪̔̏ͧͪͅl̠̙̱̋̅͛m̺̫̣̦̦͔̿͊̂ͤͬ́n̥͙̝͇̳ͤ̐̎̎̌o̥͎̩̖̾̿ͦ́p͙̹̼̫̬͔͔͕͍͔ͨ͗̇̆ͤ̽͆͗̈̐a̋͒͐͐͑̄̃̾͒͐b͈͔̦̗̜̠̪̟̘c͍̫̟͖̳͚̺͍͎͊̔̈ͣ̃͋ͦ̂ͬd͆̔ͥe̝̪͇̭̜͈͂͌͗ͬ͛͌f̰̖͓̲͔͎͔̟g̰̭͈͙̘̗͈̞͍̹̤͍͎̖̐ͨ̀̐͊̓̐ͬ̓̐͊ͩ̽͑̾ͅh̜̘ͣ͛i̥̜̣͙̥̺̥͈̦̊ͩͦ͂ͫ̂̔ͧͨj̯̪ͫ̅k̂ͪ͑͂̐͂̒̚l͇̜̫͕̩̳͖m̦̜͖̪͖̣̘̯͕͎͖ͥͭ̊͂ͦ̾̉̉̽̀̆nͦõ̏ͬ̇͗̎͌ͬ̓ͫ͌̌p̫͖̭̪̟͙̞̳̹͔͛ͯ̓ͪ̃̎̒̈́ͨͫ̚ͅa̪̱͙̮̜̳̳͎̦̗̜̺̦bc̔͂͌̽ͩ̾̋̽́ͭd̟͉̀ͫe͔̺̝̬̬f͊ǧ̩̳̲͉̺̗͕͙̲̿̐͑̔̓͂ͫ͒ͬͅh̅̋̅͐̉ͪͪͯ͑ͮͫͨͤi̮̅j͚͍̮͕̤͉̜̞͔̣͉͓̻̖̈́͆ͨ̓̐ͬͣ̿͊̎ͪ͌ͮ̓k̪̳̤̱̲̬̳͖̰̓ͪ̎̑͑̌̄̓̄l͈̜̞̪̟͚̺̫͙̦̮͙͂ͪͦͪͯ̉ͫ͑̐́ͮ͑mͤ͆n̞̹̦̱͔͍͍̟̟̳͙̪ͯͮͦͯ̌̍̇̌ͬ͐̔ͪ͊ͅoͤͥ͆̾̏̍͊ͨ̈́ͣ͆͐͋̑̅p͙͙͔̖͓̱͉͖̮͍̜̻̰̎͂̉̔̈̀̔̒̌̊ͩ̓̇aͤͣͯ̇̆̾͆̈̓ḇ̖͖c̺͓͇͇͕̪͖̠̲̲̗̜̩͖d̫͎̆̈́ͧͅe̳̺̩̱̔̍̒̽f͚͇̱̟͇̪͖͍̪ͫͦͣ́̅͐ͬ͂ͪg̍͗̀̄̇ͥ͌̓ͪͭ̋ͪhï̩̩̤̝̫̺̳͈͉̠̰̦̖̒̌ͯ̋ͨ͗ͨ́ͧ̋̏ͦj̓̃ͭ͋ͨk̜̣̥̯͈̅͂̿͛̋ḻ̯ͅmn͓̻̭̻̪̮̯̤̲ͦͧ̉͗͋̔̏͌̔ͧͅo̫̥̖͇͙ͤ͊̈ͤ̾p̜ͣabc͎̖̩d͉̥̺̩̈͂̍̿e̪͚͈ͅf̪̗̲͍͚̉̾̓ͣͨgͣͤ̄̓̑ͮ̄̎͋͛h̳̹̘̻̳̩͍̝̪ͫ͊͊̂̍̑̽̍̿i̩̫̯j͉kl̦̤̖̯̤͇̺̱̰͉m̯͖̜̻̠̣̝͚͎̬̌͊̉̈́̽̓͗͌̒ͣn̬͎̺̍͗ͭö̗p̙̭͉̞̩̑ͤ͑̄̚")
    errors += not testcase("ȧb͈̥̳͑̂ͩ͜c̴̫͙̘d̪͗ef̟̫̜̎̓ͥg̻̲̞ͪͣ̀h̲͔͉̑͑͛i̧̊j͕̝̤k͘ḷͨm̡n̻͇op̦͐́a̤̭̩ͦͮ̓͝b̗̜͌͛́c͙̐d̬̹e͕̦͌ͯf̴g̜̀h̻ͪ͘i͈̻͙j̩̹͙k͖͓̒́ľ̸̆mͦͫ̈́n͓̗̹o̘p̴̩̤a̯̝b͍̿cde̷ͭ̓̾f͡g̦̭̽̑h̼̳ͣ̚i̗ͫ͢j̃klm̛̗͑n͇̝̜͝o̰ͬp̡̫ͥȁ̪̣͙͋ͥ́bͣc̭̦̅ͬd̤ef͜g͙̽h͘ỉ̠̞͐j̃ͬ͒k̿̉ͮl̠̘̕m̱̝̫ͫͧͪn̟͎̼op̛̦̝̆̆a̞͇͎͑̓̇b̨̯̗̗̊̆̚c̱̣̩d̡̐ͩe̮̘̠f͔͉ͧ͆̕g͗ͤh̻͙̆͑͟ij̮͙͖ͮ͌ͮkl̥̇mn̼̳̮ơ̙͋p̖a̔b̳̠͐͆cͥ̓ͩ͏̳̪ͅd̻̰e̥̲fg̡̺̬̿ͬhï̵̙j͙̥ͦ͋k͚̠̾ͩl̘̣̣m̗̰ͅn͠o̟͊p̴͈͖̭ͭ̑̽a̟̝̍̈b̜̝̩̋̑͐c̼̫̏̑͡d̶͖̩̖̊̋ͬe̴͓̳͙͑̄͂f̮̮̙̾ͯ̀g̴͂̃͐h̡͚̙͒̎i̘̔j̸̺̗̭ͣ͑̾k͚̫͖̿̆̂͡l̗̰m̹̖̱ņ̍o͆̀pa͖͍̘bcd҉̞ẹ̒͞f̧̝͚̗gh͐̿ͩi̢j̵ͬ̎kl̹ͦm̺̥̐͊n̕o̖͜p̸͖͈̃̉a̞̿͜b̉̆c̫d͌e̡f͛g̨͍͍̖̾͌͌h͍̦͐̅̄ͅij̮̘́̃k̴͎̚l̀m̷̭͎͇nͬo̾pa͎͈͚ͮ̏̏b̼̤͔̅̇̔͟c̍̐͡d̎͝éfgh̢͉̺i̭͓͓͟jͩk͈̗̊̔lm̛͚͔̻̽ͭ͌n̞͍̮͑̈́̍͡o̰̙͇ͩ̐̑p̖ͫa̴̔̈́b̵c̲̝͔͌̿̈́d̙̱̬̍͒̿e̅̆f̨g̘̼̋͑h̛̼̙̟̊̏͐i̪̭j̧͇͉ͩ̾k̺͇l͍͜mnͭͫ͌͏̼̭̜opâ̋͏b̙c͞dě̶̋̿f͝g̭̰͑͛h̢ȉ̛̞͖͒jk̘̒͢l̸̰̞ṃ̸̙̠n̺̙͎ͣͥ̒o̴̪̙̍̐̚ͅp͍̟̟̈̒ͯa̼ͬb̬ͣ͝c̵d̦̚è̶͈̠̪ͫ̚f̙̯ͫͤǵh̿͏ijk̰̞̣͘l͚̳̋̍mͮ̈́͋n̛òp̶a̬̣̰b̊c̝͓͍͐̾͊de͏f̵͈̱͓͌͒̍g̘̩͋ͮhĩ̟̟ͥ͝j̟ͫ͡k͙̒l̢m̺ͥno̟̠̔̓p͉̖abcdͤ̍̈e̷f̳̙̀̍g͉̣͓̾̉̂̀hǐ̾́j̵k̭͙̭͑̉̋l̡͓̍m͑ńo̫̽p̼ã͔b́͋c̛d͍̝̀ef̡͖̙̹̆ͤͫg̦̺͐͛hij͓̰̉̚k̡̞̑ḷ̬ṁ́̚n̟̳̲op̱͝a͗͛̂b̵̙̈c͓̙ͬͣd̚e̟ͯ̕f͉ͬg̵̺͗hi̗̥͜j̍͆̆kl̼͕̃ͨḿn̹͊o̸̙̤̺͌̈̚p̝̪̮͗ͧ̆ảbcd͟ę̿ͅf̸̏g̪̠͛̾hij̀̑͂kl͞m͖n̲ͦ͠o͍ͯpa͈͌bcd͙͙ͤ͑e̜̪͉ͤ̐͒f̜ͬ́g̢hi̹̝̺j̰ͨkl͎m̗͋n̛̐o̮̾p͚̎a͛̐b̟̥͑̇c̳̬̤͆ͯͬd̕e̛f̘́ghi͇̜ͪ͑͟j̠̈́ķ̜͕͉͆̄̋l̸̩̚m̷nͭo̸ͮ̿p͚a̒̓̚͞b̷͗̃cd͈͚̖͋̇̚͝e͡f̺̤͔g̮̗̳̅̌ͭhi̡͉̘j̊kl̢̺̣̪m͙ṅ͈̭ͯo͂p͕a̟̪̩̓͋͐ḅ͊cͮ҉d̛̥̪̞̀̀͊ef̝ģ̼̟̓͌h̲̞͋̎͞i̵j̢̦̮̓ͮkl̪̭mno̦͛̈ͅp͜à̤̞̺̃̆͢bcd̙̘̬ḙ̻̘f̨g͉̈h̦̉̕i̱̗j̵k̪ͪ͠ľ̶̻̰̋m̜̑n̪̺o͖̟͒ͫp̭̭̄̊a̼̍b͓ͭ͢c͎̬̭̀d̺e͕̗̮̊ͫͥf̹͇͆̂g͖̟̅̓h̪̭ͅi̥̫̮j̆k̦͚̳ͬ̓ͦ́l͕̯̪̀mn͠o̢p̢abc͙̣̯̋̅ͪd̰eḟ͐g͝h̭͎̞i̸̖͖̱j̵kͨͮͤlͦ̀ṁ̟̬ͭn̫͉͆̍op̧̯̞ͫ̏a̝̯̮͐̓̈́bc̣̣ͯ̽d̓͗e̎f͞g̪̅h̨̰ͭi̭̝j̴̊k̴ĺ̗̳̦ͮ̊m͐n̞̊͢ǫ̃p̕a̡͓̺͈ͫ̏̒b͇͈̫ćͫ͏de̓̋f̥̪͛̎ǵh̶i̬̮͉ͦ̄ͨjk̞̻͔ͦͥ͒l̷̩̟m̖̤ͪ̅nòp̜ͭ͢a͇̭̲͂̅ͧbc͘de̲̺f͜g͕̮̮͋̅̏̕ḣ̠̝͛i̪ͦj͍̻̟̒͂ͬk͇̍l̗̻̦̒͐̔m͏n̅ͯͧopa̢̞̓b̙͇̏̈́c̐̍ͤd̀e̺̞͑̓f̢̰͚ͬ̑g̛̮h̨ijͪ́̚k̩͙̱l̫̼̎ͥ̓ͅm̃̚n̺̅opa̠̯̖͂̓̋b͍̹c̃̃d̶͕̫͇̀̓ͣe̵f̝̝͆͛͗ͅg̥̥͛ͪh̳̠͉í̼j̒͞kl̵̤̒m̓ͬͩnȯͨ͐p̌͑͋a͒̿̒҉b͐̎cd͚̹̊́e̴̊̎̏f̿͏͎g̹͗hí̜͖̞j̙̖̦ͪ͐̆k͘lm̶n̛o̘̖p̩͆́a̧̖̍b̛̝̞̺̄̊̍c̺̎de̱͗fgͩͭ̂h͖̩ͮ̆i̝͔̙j̵̺k̳̘ḻ̒mn̄̾͌ọ͊p͍̟͚a͟b͟c̼̠d̼ẹ̢̔f̳͚͉ͭ͋̀ǵ̸ͭh̨i̵̋̈̒j̼̲͌ͦkl̼͙ͅm͙̟͕̍ͮ̒n̹͋ô̵ͥpͪ̌̂͏aͥͣͣb̚̕cdefͬ̋g͍̳͑̈hi͙͓ͮ̒jͨk͛l̘̦̹ͬ͒̑m͕̠̞ͫ̅́n̢ͦͪò͕͈̅͢p̴a͎̮͍ͭͭͤb́c̏deͮ̔̇f̥̲̗ǵ̪h̽ij͔͆ķlṃ̲̼̀̀̒nͨͪ͘o͍ͫp̖͕͎̎͑̚͝a͙̻͓ͨ́͋͡b̩ͤc̣de̴̤͓̙̎̃ͩfg͔hi̞j̴kl͞m̫̔n̮̈́͝o̢̝͓ͭ̅p͉̍ab̞͒c̿de͈ͩf̡̤̙g̱h̪i̫̗ͣ̈́j̟͘kͥͨlmn̶op̞̰̭ͤͭͥabcd̯͕̫ͫ͌ͬe͏fg̰h̢̝ͨͦͅi̟j҉kl͖͚ͯͨmn̡̹̭̞ͬ̇ͦo̞̞̱ͣ̀̈͜p͉̜̬a̢͇̰b̼̻͇̒̊̍çͨde͡f̠̰͈͛ͩ̚̕g͍̠͛̂h̫̗ij͓ͭ͜k͚̯̟l̻͚̥mͤ̍͏͈̪n͙ͨop͝ḁ̝b̸cd͛e͔ͬf̥͋ghi̿̿̚j͇k̄̏͑lm̰̞̠̈͗ͮṉop̧ȁ̶̒b҉͉͖c̛̜͖̳d̥ͩeͧ͋f͔ͯ̀g̩̈́h̻̘̪͂̔̈i͏̯jͤ̒ḱḷm͢nͮ̃̌ó̥͢p͏̱͉̘ȁ͇͇̒bc͙͙d͒҉̜e̙̞f̜̼̲̓̊ͩ͞gͬh̦̻͈ͤͫ̒͡ij͂̀̄kl͡mn͞õ̲pa͝b̠͍͐̽ͤͅcde͋ͧf͟g̨ͩh̶̾͆i̋ͯjkl͘mn̰op̄̍͆ǎ̺͘b͍̙ͧ̿c҉d̞͘e͓ͥf̣̻̀͒ğ̼̼̇h̩͖̱̓͆̚ij̗̞̬ͯ̿̇kl̷m҉n̪͖̓ͦō҉p̼̗ͯ̔a͍̔̕bc͎͉̹ͦ̑ͨ͘ḏͭe̴f̖͉̳ͣ̽̌͠ğ̗̼ͨḥ̎ͣͭ͢ͅͅi̼̤j̧kͨ̍͐l̹̙̠̓̒͆m̕n̨o̘̎p҉͈a̡͛̚b̤͍̕cd̠͓̥̓̃̃e̡f̮ͦg̣h̒͑͏ḯ͚͈̫̎̇j̡̲ḱl͉̠ͩ͌͟m̐̔̚n̸o̱̕p̲̈͜ab̉ĉd̪͎̀͋͌͢ͅȇ̺fghi̋̂̅j̨͓̮ͭ͂kl͘m̭̀ṅ̻̥̣̍̅o͕ͫp͇͗a̠̤͖͐͛͌bc̀d͍̆́efͣ̎͊ǵ͚̖̋́h͡ij̓͐ͩkl̳͌m͛̇̏n̲̑̕op̧̮̈ả̗͔̤̉ͮ͞bc̛̥̠̳͌̾̓de̯͈̰f̖̺͚gh̪̤̅̅i̹̙̹j̖̹̎͗k͎̓l̟̜͑͋m̶̺̙̬ñ͕̱̾op̿ͫ̐ab̧͔̎ć̰͠def̺̠̦̄̿̌ģ̙͓̺̈̽ͧh̑ij̴kl͠mn̖̠ͪ̌op̋ͪab̿̓cd̋ͧ̃e͗fg̘̗̐̀́h̡ijk̘̪͂͗l͎̦̍ͤm̀n͉̤o͡pab̖͎͔c̼͂d̷͖̤̮́̍̏e̱̟͛͊́f̠̦́g̒̆h̔i̊͝j̤̥̙ͯ̇ͭk̬̳̤ͥͣ̒͡l̺͇ͦ̆m̠̞̻̑ͯ̚n͗ͪ̐o͇̪̔̂p̢̬͈̯a̰̼̍ͫb̶c̩̟̫̈́̽́̚d͆̾̐ef̣̆g̢̬̮hi͓̲͒͆jk̨lm͎̊nòp͎̀abc̩d̻̅͘efg͖̩͆̍hiͥjk̛l͓̻̄̊m̛ṅ̜̣ͮo̸p̝̗̩͗́ͦa̺͓bc̈d̯̱̫͆̑ͩe̬͐fg̕h̵ì̮̙̄̀j̰̹͌͗kl̠̰ͧͥ̀m̯͖̪͗̃̊͝ņ̤̠̂̾ȍ̠͓̔͠p̟ͥ̀͟ͅąbc͑̉d͢e̱̖̦͛ͦ̈͟fg̰͐h̷͍͚i̮̳͝j͖͕͉̈́̐͑͞k͏̹̮lm̶̪̘̩̒͋̄n̲͈̍̚opͤ̋͛ả̲b͚͡cdͣẻ̦͠f̯̖̜͊ͯ́g͔͆h̝̩̞ͦ̈̀i̘̓j͇̠̥͝k̍͌̍͏̖̭̻l̰̰̇̄͞m̧̦ͪn̉̉̀҉̗̥͚o͊̈́ͭp͆͑͗ạ̷̿b̯͕̳c̖ͫd̸e̯̯̓̊f̘͌ġh̼i̬̖j̢̫̰̀͆k͞lm͎̈́͘ṋ̡͎̌̅ö̩͇̮͂ͬ͞p̹͇̦̾ͫͧàb̛c̯͍͉ͯ́ͮd̨̩̖̥͐ͬ̀e̯͙ͪͩ͝fͤgh̸̤̲͍̏ͫ͒i͚͓̳̅ͥ̃jk͑̚l̾m̿͐nopa͢b̨̿ͩc̣̪͙̈́͂̂̕d̔̐e͠f̢͒ͤ̓g̦̞̯ͧ̒̂h́i̾͢j̼͓̫̑͋̓͡k̶͍͗lḿ̸͇̰̝̄̊nͣ̅̚ő̤̗͒p̠̰͈ͮ̓ͥa̡ͮ͑̑b̽̒ͤc̆̌͡d̿ef̨̮̼̫͊̄̈́g͇͜h̠̣̊̓̚ͅi̿̔҉̮͎j̪̣̹̽́ͯk̬l̄mͤno͓ͫp̬̹̹̆͛͒͘ab̸̳cdͤͣ̒҉ē͓͙̊f̬ͩg͂̀̄h̊ͣͨi͓͕͇j̽ḱ̲͔̼̾̀̚l͙m͍̦̿̉͢n͛o̡̮̹͕ͫ̎̂p̭̭̭̊̐̄a̜͛b̧͈̤ͧ̿c͆ͦ̿͠d̦̭e̩̫͛ͪfg̝̯ͥ̃h̀i̶͈̪͗ͫj͡k͢l̄ͫmno̳̫̽ͫp̔̔a̪͘ͅb̞̂c̐̀̾d͆̽̀e͙fg̖͛h̀i̵̺͙ͥͦjḱ͏̰l̻ͪmn͍̖̎ͬo̼̥̘ͨ̑̊̕p̭̫͎̉ͧͨab̳̆c̝̣̯̊͊ͣḋ̟̮͑e̟̭̤f̋ͦ̔g̓͝hi̬͉̅̄j̫̊͘k̖͍͆̉l̠͛m̴̆n͍͕̯̕o̖͖̹͒ͣ͐p̴͓a͟b̸̖͍̞͋̎̍cḑ̦eͦ̃̐͏f̹ͬgͬ̅͝hͩ̔ï̱j̩̣̯͋ͬͤ̀kl̰̝̅̈́m̫̠̟n̄̅͢o͑͒͑p̳̥̦̉̔͆aͅb̘̪ͦ͊c̗͓͉d̄̉̂ē̱̫̈f̩̥̤̅̓ͯg̥̙͐͆͝h̩̞͓ij̷̫͔̖k̫͎͍ͩ̒̊lm͔͋ṉ̗̰ͥͭ͑o̸͚͈̣p͓̯̆̈́̀a̵̫͙ͭͬbc̎ͥ͗͢d̩̗é̤̕f͖̤͊̐g͐̎ͨh̶i͎̅j̴k͖̱̘̊̅͗lm̲̰ͭ̈n̛̤̮͍o͔͌p̭̂̃ͅa̪b̮͔͆̋c͈̲̫̒̆̚d̘ͫef͈̈́ĝ̖h̦̭̦̑ͧ̃͘i̧j̱̞̒̊k̎̒l̶͎̖̆̿m̯͖̏͗nͧ̈́ǒͅp̧a͜ḇ̨̭̯c̠̏def̮̙̰̍͐̔g̲̞͋͛h̡̜̜̣̔̅̔ḭ̂͟j̙̭̈́̅k̗̝͊͌l̥̃͜m̓̊ͤṋ̩̮͆͊ͥo̵̼̣̔̾pa̛͋b͚̻͒ͥc̒͒̽d͚efģh͠ȋ͉̮͕́ͧj̲́ͮ͟ͅk̛l̼̘̿̒m̼͑n̫̱ͤ̋ͦͅo͑͌̽p̲̽a̲̭b̻̖̜̒ͧ͂cdẽ͖f̩̻̞ͯ͆̽g̺̣hi̯̿jk͟l̟̭̫͜m̯͑n̡͓͇̺̔̐͗o̡̱p̃̊ͮ͏ảͭb̸͑c̰̜̆̍ͦͅd͕ͥe͎ͬf̠̀g̠͎̖͂̓̃hi̙̫̗ͣͮ̊j̺̰̝̔ͧ̓͝ḱl̮̳m̙͕̠͡ņoͨͣ̌p̶͍̎a̦̕b̤̘̾ͧcd̟̠̞͂́ͨef̷ğ̂h̷ij̛k͈ͤ̓ͅl̽ḿ̂͠nͦoͪp̘͢ab̺̊cͬ̓͘d̘̿e͠fg̛̔ẖ̭̫̑̇́ḯ̺j̘̯ḱ͕͟l̲m͖̫͜n̴o̫ͮp͍̹̬̉͆͊ā̱̱̀b̾̕c̯̥͇defg̕h̛͔́i̛̯͑j̷͖k̴̼̒l̝̉m͐͊nȯͪ͑p͖̺̒̐̕a̽ͫ̓͏b̍ͭ̚c͙̞̭͆̒̿͞de͢fg̹ͯ͜h̖̩̳̐ͫ̄ij̪̩̩klm͖͈ͧͤnȏ̮̰̈̌ͅp̣̣͈͋̈ͫa̝̤̰b̡̝̤c͂͗̚͞de̤̺̗͐͒̑́f̫̉͞g̈ͦ̕hͣ͆̿i͛͜j̩k̤̼̋̉lm͞n͎̟̈̆op̱͑a̳ḅ̶̳̃ͮc҉̯͎d͓͉̝͐̈̚e͙f͝g̤͌ḧͬi̮̐jk̮̤̊̿͜l̙m͐̓͌n͜o͏p̜̼͉ͯ͑͒͘a͙͆b̡͔č̴̳͈̽͒ͅd̻̮̟e̱̥͉̓̆ͭfgh̺̒͝ij̒ͥk̀ͮ̾́l̥ͧm̪nopͮaḃ̤̕cd̟̗͈̉͌͒́eͨͯ͒̕f̼͇͒̋g͐҉h͝ijk̵̖̙̭l̷mno̜͉͍p̴̳͔̭̓̅̀ab̗̱̎̄cd̼͈̪̉ͥ̒ē̳͔̹͊̅f̵g̶̠̔h̛ij͓̮̥̔̎̽kͥ͌́lm͏n̵o̤͓̽̄pa̤̬b͔͔̀c̫̱d̰͎ͮͮef̕g͟hiͭj̜͊k͎ͦl̰̤ͮ͛͞mn̮̰o̚p̉̎ͤ͏̬͙̞a̼̖͓̔́̾bc̨̹d̻̰ͭ̑͋ͅe̱͈̻ͦ̒ͪf̸̤͇g͝ḩi͍͓̘ͫ̈́̎jk̵l̻̥̘͆̃̓mn̢o̹͉͊͋͌̀ͅp̬̫̀ͅa͎ͯ͡b̮͔̥̄ͦ̃c̠̺͛̆d̷̞͊ef̟́ĝ̠̂͟ͅh̵͉ͧi̛̍́j͓ͤk͢lm̸̞n̆͂͗o̴̝̬͗ͣͫͅp̯̊a̷̭̞ͪ̓bc̰̑͝dḛ̿f̝̺͚̑͂͌͡g̖hijk̦ͯl̩͇̦ͭͤ̓m̧͚̾n̡̩͓op̵̣͍̘͒̿ͨã͕͓̪́̀͝bcd̝͇̘͞ef̢̦͓͂̀g̰͓ͫ͒h͢ijk̸̰͈ͪ̌l̛m̄̓̃҉no̴p͟ấ͈̳b̴̼͉̖c̼̻ͭ̀ď̗ḙ͚ͣ̋f̀ģhi̙̘̽͒j͔̮̈͗kl͓̼̞ṁ̮̕no̪pabc̏̆͝d̴ef̧̻̪̗ͣ͊̂g҉̦̠hij̍̓ǩ̥͔̳̓͋l̼m͙̎n̪̲o̪͠p̬͓ąͤͯ̑b̛c̖͔̖ͣ̏ͨdefgẖ̘̝͌̔̊ijk̽̿l̞̰̑͋m̪̈n̮ͥ͠ǫ̯͈p̼͙̝a̛͑̄b̸̪̺͌͆c̛d̠̼͔̍ͬ͒e͓fg͘ḥ͐i̜͔͑̋̕j͓͎̦́̅ͭ͢k̼̇l̡m̥͔n̡̖͂o̮̖pͩa̶b̤͍͇͢c͓̖͗̊d̙ͧẽ̞f̦ġȟ̀ͧ͝ī͙̜̆j̴̋ḱ̏lmnͯ̀o̡p̵a͙̅b̞͑c̼̬̖̉̌ͮdê̸̺͉̿f͎̩ģh͈̺͚͗ͯ͒͟ij̜̚͝k͍l̹̳̑ͭ͢ḿ̬͕͒n̙ͧ͡op͋̄̒a͜b̹̝̙͆ͩ̊͝c͋ͧd̓̿ͦĕ̶͔fĝ͔̲̚h̼̦͕i̳̘̓̿jͫ̚k͚ͬl̢̋m̲̍n̳͇opa̷b̛c͓͇͍͛ͫ̂d̩̳͈͆ͪͯe͢f̦̲g͖̣h̵̟̻̘ͪ̈̇i̵j̾ḱlmͣnͪ̐ͯ͝op̗͈ͧͯàbc̀d͡ef̯̺̣g͡ḫ̃̀ḯ̾j͙̲̳k̂ḻ̙̈́͊m̕no̩͕̝͌͆ͣpa͎̻͚̿ͥͩb̭̋c̘͍̓͂d̔̂ef҉g̫̤̣̓̏̀h̶̼ͭi̮ͩ͝j͍̟͉̓ͦ͛k͎̫̲͂ͫ͒lmͬ͠ń̮o͉ͭṗ̰͘ả͕̝̩͌̂b͕͎̱ͯ͗̾c̦d͠e͔̬͓̽̔̑f̥̂g̞ͭh҉ì̗̣̽jk̭̬̰ĺm͢n͚̱̰o͗̓̊p̋͆͒ā̖͜bͨ̿̅c͂ͪ͏͚̜ḍ̨̜ͅef̷g̸hͭ͆͏i̛̙ͫj̮̭̎ͫk̙̩̟̊̇̉l̸m͚̽n̨͔̥̯o̞pá͓̖ͥ̔ͅḅ͚̪̉̋ͥcd͈̣̒ͩḙ̤̂͒͢f͎̚g̮̬ͪͬh̛̬̼̐̏i͈͢j̭͖ͫ̆k̲͙̞̇̊̂lm̪͕͛̍n̂ͫ҉̣̣op̗͘àb̧͇͐c̸ͩ͌͊dͩ̈́ͬe̱̝ͩͮ͠fg̟h̴ij͌͌͠k̞̞lm̢̠͍̠noṕ̷̰ab̝̝͒̄̕c̨̘͇d͕͟e͚̜͔͢f̰͋͢g̋́hijk͇̏l͗ͤm͟n͕͈o̜̥͑ͮp̭̳̫a̖̯͑ͩbͧc̝ͤd͂͂ë͓̲̞́̊̐f̋g͛̅h̩̫̹̿̾̈i̼j͖̺̱̍͂͋k͕ͩ̕lmͯͫn͝o̴p̭̝̻͗͒̿å̧̞̲ͭb͓cd̲̠͡ͅef̓ͤg̅ĥ̬̩̖̍̈i̲̣̊ͨ̕j͎̠̉ͭk̮̺̼͑͗ͮl͞ḿ̩͟n̼̊o͖p̯̜̗ͨ͐ͯa̢b̭c̴̰͔̦̓̋ͭḓ͖͋̚e̶͉ͯf̣̪̀̽g͎͇̖h̨̫̙i͢j͕̖͔́̾͂k̢̳̗͕͋ͪ͐l͗͂m̹͎̗̂͆̍n̢̮ͭóp͔̩͂ͭ")
        
    print(f"Тестирование завершено, количество ошибок: {errors}")

    sys.exit(errors)

main()
