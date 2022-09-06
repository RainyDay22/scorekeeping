#include <iostream>
#include <string.h>
#include <fstream>
#include <map>

int init_file(std::string filename, std::fstream* file);
int init_scbd(std::fstream* file, std::map<std::string,int>* scbd) {return 1;};
void edit_ptcp() {};
void edit_pts() {};
void print_lboard() {};
void save() {};

int main(){
    //init vars
    std::string f_name; //filename
    std::fstream* score_file; //scoreboard file
    std::map<std::string,int> scbd; //real time scoreboard data structure

    // welcome message + list of possible actions
    std::cout << "Welcome to scorekeeper!";

    // require storage file name/creation => load/create
    while(true) {
        std::cout << "Input storage filename";
        std::cin>> f_name;
        if (init_file(f_name, score_file)) 
            break;
        std::cout << "Error. Try again.";
    }


    if (!init_scbd(score_file, &scbd)){
        std::cout<<"score_file load error";
        return 0;
    }

/*
    // give rundown of possible actions
    std::cout<<"Possible actions: participant+/-, points+/-, print, save";

    // for loop to process argument, read until endl
    std::string line;
    while (std::getline(std::cin, line))
    {
        std::cout << line << std::endl;

        if(line=="exit") break;

        char action ='o';
        if(line.find("ptcp")==0) action='a';
        else if(line.find("pts")==0) action='t';
        else if(line.find("print")==0) action='r';
        else if(line.find("save")==0) action='s';
        else action='x';

        switch(action){
            case 'a':
                edit_ptcp();
                break;
            case 't':
                edit_pts();
                break;
            case 'r':
                print_lboard();
                break;
            case 's':
                save();
                break;
            default:    
                std::cout<<"please enter a valid command"<<std::endl;
        }
    }
    // break loop at "exit" keyword
    // process arguments + prompt if needed (i.e."add", please input name "Name Lastname")
*/
}

int init_file(std::string filename, std::fstream* file){
    std::cout<<"filename is: " << filename <<"*" <<std::endl;

    if (!filename.length())
        return 0; //whack rn but it's okay

    std::fstream* temp = new std::fstream();
    temp->open(filename, std::fstream::in | std::fstream::out);
    if(*temp) {
        std::cout<<"file exists";
        file = temp;
    } else {
        std::cout<<"file creation initiated";
        std::fstream* new_f= new std::fstream;
        new_f->open(filename, std::fstream::out);
        // if (!*new_f) {
        //     std::cout<<"error in file creation"<<std::endl;
        //     return 0;
        // }
        file = new_f;
        new_f->close();
    }
    temp->close();
    return 1;
}