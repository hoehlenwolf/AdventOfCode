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
#include <string.h>


EXPORT int calcNthNumber(int n, int* starting_numbers, int starting_numbers_length) {
    int* spoken_numbers = (int*)malloc(n * sizeof(int));
    // Set all entries in array to 0
    memset(spoken_numbers, 0, n*sizeof(int));
    // initialize next number to be spoken and helper value
    int number_to_be_spoken = 0;
    int help = 0;
    // Prepare starting numbers
    for (int i = 0; i < starting_numbers_length; i++) {
        // Starting number at index i is spoken at turn i+1
        spoken_numbers[starting_numbers[i]] = i + 1;
        // number to be spoken next is the starting number at index i itself
        number_to_be_spoken = starting_numbers[i];
    }

    // Loop through all turns
    for (int turn = starting_numbers_length; turn < n; turn++) {
        // Turn in which the number_to_be_spoken was previously spoken (0 => not spoken before)
        help = spoken_numbers[number_to_be_spoken];
        // Set the turn number when number_to_be_spoken was last spoken to current turn number)
        spoken_numbers[number_to_be_spoken] = turn;
        // if number_to_be_spoken hasn't been spoken before
        if (help == 0) {
            // next number_to_be_spoken is 0
            number_to_be_spoken = 0;
        }
        else {
            // otherwise its the difference between current turn number and turn number when old number_to_be_spoken was last spoken
            number_to_be_spoken = turn - help;

        }
    }
    // free memory
    free(spoken_numbers);
    // return the n-th number to be spoken
    return(number_to_be_spoken);
}


int main(int argc, char** argv) {
    // Starting Numbers for debugging
    int starting_numbers[] = { 20, 0, 1, 11, 6, 3 };    
    int starting_numbers_length = 6;
    printf("Running with (default) starting values [");
    for (int i = 0; i < 6; i++) {
        printf("%i,",starting_numbers[i]);
    }
    printf("]\n");

    // Get the result for default starting numbers
    int result = calcNthNumber(2020, starting_numbers, starting_numbers_length);
    printf("Result (Part A): %i\n", result);
    result = calcNthNumber(3E07, starting_numbers, starting_numbers_length);
    printf("Result (Part B): %i\n", result);
    return 0;
}
