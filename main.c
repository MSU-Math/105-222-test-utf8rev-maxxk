#include <stdio.h>

// функция "считать следующий корректный символ"
// считывает корректный символ из потока input
// возвращает EOF, если считать не удалось
// (кончился поток ввода)
// возвращает 1 и записывает ответ по указателю result,
// если считать удалось
int read_next(FILE *input, char *result);

int main(void)
{
    char first;
    char second;

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

int read_next(FILE *input, char *result)
{
    (void)input;
    (void)result;
    return EOF;
}