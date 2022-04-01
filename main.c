#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define LIM 128
#define UTF 4
#define FIRST_TWOBYTE 0xC0
#define FIRST_THREEBYTE 0xE0
#define FIRST_FORUBYTE 0xF0
#define INITIAL_SIZE 4

#include <stdio.h>

// функция "считать следующий корректный символ"
// считывает корректный символ из потока input
// возвращает EOF, если считать не удалось
// (кончился поток ввода)
// возвращает 1 и записывает ответ по указателю result,
// если считать удалось
int read_next(FILE *input, unsigned char result[UTF]);
int read_continuation(FILE *input, unsigned char *result);

struct dynamic_array {
    int size;
    int capacity;
    int *values;
};

void insert(struct dynamic_array *array, int value);

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

int read_continuation(FILE *input, unsigned char *result)
{
    int text = fgetc(input);
    if (text >= LIM && text < FIRST_TWOBYTE) {
        *result = (unsigned char)text;
        return 1;
    }

    ungetc(text, input);
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
            if (text < FIRST_TWOBYTE) {
                continue;
            }
            *result = (unsigned char)text;

            if (!read_continuation(input, result + 1)) {
                continue;
            }

            if (text >= FIRST_THREEBYTE &&
                !read_continuation(input, result + 2)) {
                continue;
            }

            if (text >= FIRST_FORUBYTE &&
                !read_continuation(input, result + 3)) {
                continue;
            }
            return 1;
        } else if (text == EOF) {
            return EOF;
        } else {
            *result = (unsigned char)text;
        }
        return 1;
    }
}
void insert(struct dynamic_array *array, int value)
{
    if (array->capacity == 0) {
        array->values = (int *)malloc((INITIAL_SIZE) * sizeof(int));
        array->capacity = INITIAL_SIZE;
    }
    if ((array->size + 1) >= array->capacity) {
        int *expanded;
        expanded = (int *)malloc((array->capacity) * (sizeof(int) * 3) / 2);
        memcpy(expanded, array->values, array->size * sizeof(int));
        free(array->values);
        array->values = expanded;
        array->capacity =
            (int)((array->capacity) * (sizeof(int) * 3) / 2 / sizeof(int));
    }
    array->values[array->size] = value;
    array->size = array->size + 1;
}
