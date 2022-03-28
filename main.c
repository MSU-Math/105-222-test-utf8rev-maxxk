#include <stdio.h>
#define LIM 128
#define UTF 4

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
    
    unsigned char first[UTF];
    unsigned char second[UTF];

    while (1) {
        if (read_next(stdin, &first) == EOF) {
            break;
        }

        if (read_next(stdin, &second) == EOF) {
            fputs(first, stdout);
            break;
        }

        fputs(second, stdout);
        fputs(first, stdout);
    }

    return 0;
}

int read_next(FILE *input, unsigned char *result)
{
    for (int i = 0; i < UTF; i++) {
        *(result+i) = 0;
    }
    while (1) {
        int text = fgetc(input);
        if (text >= LIM) {
            // 1100 0000
            if ( text < 0xC0) {
                continue;
            }
            *result = (unsigned char)text;
            int skip = 0;
            int count = 0;
            if (text >= 0xF0) {
                count = 4;
            } else if(text >= 0xE0) {
                count = 3;
            } else {
                count = 2;
            }
            for (int i = 1; i < count; i++) {
                text = fgetc(input);
                if (text >= LIM && text < 0xC0 ) {
                    *(result+i) = (unsigned char)text;
                } else {
                    ungetc(text, input):
                    skip++;
                    break;
                }
             }
            if (skip == 1) {
                continue;
            }
        }
        // 1110 0000 E0 1111 F
        if (text == EOF) {
            return EOF;
        }
        *result = (unsigned char)text;
        return 1;
    }
}
