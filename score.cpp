#include <iostream>
#include <string.h>
#include <fstream>
#include <vector>
#include <sstream>

using namespace std;

std::fstream* init_file(std::string filename);
int load_file(std::fstream* file, std::vector<vector<string> >* container);
void print_table(std::vector<vector<string> > table);
void edit_ptcp() {};
void edit_pts() {};
void save() {};

int load_file(std::fstream* file, std::vector<vector<string> >* container) {
    //std::vector<vector<string> > content;
    std::vector<string> row;
    std::string line, word;
    
    if (!file){
        cout<<"load_file file segfault"<<endl;
        return 0;
        }
    if (!container){
        cout<<"load_file container segfault "<<endl;
        return 0;
        }

    //file->open();
    if(file->is_open()) {
        while(getline(*file, line)) {
            row.clear();
            std::stringstream str(line);
    
            while(getline(str, word, ','))
                row.push_back(word);
            container->push_back(row);
        }
    }
    else{
        std::cout<<"Could not open the file\n";
        return 0;
    }

    return 1;
    }

    void print_table(std::vector<vector<string> > table){
        for(int i=0;i<table.size();i++) {
        for(int j=0;j<table[i].size();j++){
            std::cout<<table[i][j]<<" ";
        }
        std::cout<<"\n";
        }
    }


int main(){
    //init vars
    std::string sf_name; //scoreboard filename
    std::fstream* score_file; //scoreboard file
    std::vector<vector<string> > scbd; //real time scoreboard data structure

    //rubric is optional
    std::string rf_name;
    std::fstream* rubric_file; 
    std::vector<vector<string> > rubric;

    // welcome message + list of possible actions
    std::cout << "Welcome to scorekeeper!";

    // require scoreboard file name/creation
    while(true) {
        std::cout << "Input storage filename: ";
        std::cin>> sf_name;

        score_file = init_file(sf_name); 
        if (score_file)
            break;
        std::cout << "Error. Try again.";
    }
    
    //load scoreboard file
    if (!load_file(score_file, &scbd)){
        std::cout<<"score_file load error";
        return 0;
    }

    // give rundown of possible actions
    std::cout<<"Possible actions: participant (ptcp)+/-, points (pts)+/-, print, save"<<endl;

    // for loop to process argument, read until endl
    std::string line;
    while (std::getline(std::cin, line))
    {
        
        if (!line.length()) continue;
        if(line=="exit") break;

        char action ='o';
        if(line.find("ptcp")==0) edit_ptcp();
        else if(line.find("pts")==0) edit_pts();
        else if(line.find("print")==0) print_table(scbd);
        else if(line.find("save")==0) save();
        else std::cout<<"please enter a valid command"<<std::endl;
    }
    // process arguments + prompt if needed (i.e."add", please input name "Name Lastname")

    score_file->close();
    //rubric_file->close();
    delete score_file;
    delete rubric_file;
}

std::fstream* init_file(std::string filename){
    std::cout<<"filename is: " << filename <<"*" <<std::endl;

    if (!filename.length())
        return nullptr; //whack rn but it's okay

    std::fstream* temp = new std::fstream();
    //file = temp;
    temp->open(filename, std::fstream::in | std::fstream::out);
    if(*temp) {
        std::cout<<"file exists"<<endl;
        //cout<<"temp is"<<temp <<endl;
        //return temp;
    } else {
        std::cout<<"file creation initiated"<<endl;
        std::fstream* new_f= new std::fstream;
        new_f->open(filename, std::fstream::out);
        // if (!*new_f) {
        //     std::cout<<"error in file creation"<<std::endl;
        //     return 0;
        // }
        //file = new_f;
        //new_f->close();
        temp->close();
        return new_f;
    }
    //temp->close();
    return temp;
}