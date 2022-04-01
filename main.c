#include <stdio.h>
#define LIM 128
#define UTF 4
#define FIRST_TWOBYTE 0xC0
#define FIRST_THREEBYTE 0xE0
#define FIRST_FORUBYTE 0xF0

#include <stdio.h>

// функция "считать следующий корректный символ"
// считывает корректный символ из потока input
// возвращает EOF, если считать не удалось
// (кончился поток ввода)
// возвращает 1 и записывает ответ по указателю result,
// если считать удалось
int read_next(FILE *input, unsigned char result[UTF]);

int main(void)
{

    unsigned char first[UTF];
    unsigned char second[UTF];

    while (1) {
        if (read_next(stdin, first) == EOF) {
            break;
        }

        if (read_next(stdin, second) == EOF) {
            fputs((char *)first, stdout);
            break;
        }

        fputs((char *)second, stdout);
        fputs((char *)first, stdout);
    }

    return 0;
}

int read_next(FILE *input, unsigned char result[UTF])
{
    while (1) {
        for (int i = 0; i < UTF; i++) {
            *(result + i) = 0;
        }
        int text = fgetc(input);
        if (text >= LIM) {
            // 1100 0000
            if (text < FIRST_TWOBYTE) {
                continue;
            }
            *result = (unsigned char)text;
            int skip = 0;
            int count = 0;
            if (text >= FIRST_FORUBYTE) {
                count = 4;
            } else if (text >= FIRST_THREEBYTE) {
                count = 3;
            } else {
                count = 2;
            }
            for (int i = 1; i < count; i++) {
                text = fgetc(input);
                if (text >= LIM && text < FIRST_TWOBYTE) {
                    *(result + i) = (unsigned char)text;
                } else {
                    ungetc(text, input);
                    skip++;
                    break;
                }
            }
            if (skip == 1) {
                continue;
            }
        } else if (text == EOF) {
            return EOF;
        } else {
            *result = (unsigned char)text;
        }
        return 1;
    }
}
