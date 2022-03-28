#include <stdio.h>
#define LIM 128

#include <stdio.h>

// функция "считать следующий корректный символ"
// считывает корректный символ из потока input
// возвращает EOF, если считать не удалось
// (кончился поток ввода)
// возвращает 1 и записывает ответ по указателю result,
// если считать удалось
int read_next(FILE *input, unsigned char *result);

int main(void)
{
    unsigned char first;
    unsigned char second;

    while (1) {
        if (read_next(stdin, &first) == EOF) {
            break;
        }

        if (read_next(stdin, &second) == EOF) {
            fputc(first, stdout);
            break;
        }

        fputc(second, stdout);
        fputc(first, stdout);
    }

    return 0;
}

int read_next(FILE *input, unsigned char *result)
{
    while (1) {
        int text = fgetc(input);
        if (text >= LIM) {
            continue;
        }
        if (text == EOF) {
            return EOF;
        }
        *result = (unsigned char)text;
        return 1;
    }
}
