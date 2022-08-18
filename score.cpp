#include <iostream>
#include <string.h>


int init_file(std::string filename){
    //if starts with - then create new file 
    //else, check if file exists
        // if read/writeable return 1
        // if no existence or wrong permissions 
        return 0;
}

int main(){
    //init vars
    std::string f_name;
    
    std::cout<<"Hello World";
    return 1;

    // welcome message + list of possible actions
    std::cout << "Welcome to scorekeeper!";

    // require storage file name/creation => load/create
    while(true) {
        std::cout << "Input storage filename or type '-Bob' to create a new file with name Bob ";
        std::cin>> f_name;
        if (init_file(f_name)) 
            break;
        std::cout << "Error. Try again.";
    }

    // give rundowm of possible actions
    std::cout<<"Possible actions: participant+/-, points+/-, print, save";

    // for loop to process argument, read until endl
    // break loop at "exit" keyword
    // process arguments + prompt if needed (i.e."add", please input name "Name Lastname")
    // switch statement

}
