#if defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)
#ifdef __cplusplus
#define EXPORT extern "C" __declspec (dllexport)
#else
#define EXPORT __declspec (dllexport)
#endif
#else
#define EXPORT
#endif
#include <stdlib.h>
#include <stdio.h>


EXPORT int calcNthNumber(int n, int* starting_numbers, int starting_numbers_length) {
    int* spoken_numbers = (int*)malloc(n * sizeof(int));
    int number_to_be_spoken = 0;
    int help = 0;
    // Initialize all values as -1
    for (int i = 0; i < n; i++) {
        spoken_numbers[i] = -1;
    }
    // Prepare starting numbers
    for (int i = 0; i < starting_numbers_length; i++) {
        spoken_numbers[starting_numbers[i]] = i + 1;
        number_to_be_spoken = starting_numbers[i];

    }
    // Loop through all turns
    for (int turn = starting_numbers_length + 1; turn <= n; turn++) {
        //printf("Turn %i, spoken num from last round %i\n", turn, number_to_be_spoken);
        if (spoken_numbers[number_to_be_spoken] == -1) {
            //Number hasnt been spoken yet
            spoken_numbers[number_to_be_spoken] = turn-1;
            number_to_be_spoken = 0;
        }
        else {
            help = spoken_numbers[number_to_be_spoken];
            spoken_numbers[number_to_be_spoken] = turn-1;
            number_to_be_spoken = turn - 1 - help;

        }
        //printf("Num to be spoken: %i\n", number_to_be_spoken);

    }
    free(spoken_numbers);
    return(number_to_be_spoken);
}


int main() {
    // Starting Numbers for debugging
    int starting_numbers[] = { 20, 0, 1, 11, 6, 3 };
    printf("Running with starting values [");
    for (int i = 0; i < 6; i++) {
        printf("%i,",starting_numbers[i]);
    }
    printf("]\n");
    // Get the result for default starting numbers
    int result = calcNthNumber(2020, starting_numbers, 6);
    printf("Result (Part A): %i\n", result);
    result = calcNthNumber(3E07, starting_numbers, 6);
    printf("Result (Part B): %i\n", result);
    return 0;
}
