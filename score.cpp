#include <iostream>
#include <string.h>
#include <fstream>
#include <vector>
#include <sstream>

using namespace std;

std::fstream* init_file(std::string filename);
int load_file(std::fstream* file, std::vector<vector<string> >* container);
void print_table(std::vector<vector<string> > table);
void edit_table(std::vector<vector<string> >* container, std::string input);
void save_file(std::fstream* file, std::string filename, std::vector<vector<string> > table);

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
    std::cout<<"Possible actions: 
        edit scoreboard (scbd), 
        edit rubric (rubric), 
        print, 
        save"<<endl;
    //add rubric print n save
    //add option to repeat action list

    // for loop to process argument, read until endl
    std::string line;
    while (std::getline(std::cin, line))
    {
        
        if (!line.length()) continue;
        if(line=="exit") break;

        char action ='o';
        if(line.find("scbd")==0) edit_table(&scbd, line.substr(5));
        else if(line.find("rubric")==0) edit_table(&rubric, line.substr(7));
        else if(line.find("print")==0) print_table(scbd);
        else if(line.find("save")==0) save_file(score_file, sf_name, scbd);
        else std::cout<<"please enter a valid command"<<std::endl;
    }
    // process arguments + prompt if needed (i.e."add", please input name "Name Lastname")

    score_file->close();
    if (rubric_file!=nullptr) rubric_file->close();
    delete score_file;
    delete rubric_file;
}

std::fstream* init_file(std::string filename){
    std::cout<<"filename is: " << filename <<"*" <<std::endl;

    if (!filename.length())
        return nullptr;

    std::fstream* temp = new std::fstream();
    temp->open(filename, std::fstream::in);
    if(*temp) {
        std::cout<<"file exists"<<endl;
    } else {
        std::cout<<"file creation initiated"<<endl;
        std::fstream* new_f= new std::fstream;
        new_f->open(filename, std::fstream::out);
        temp->close();
        return new_f;
    }
    return temp;
}


int load_file(std::fstream* file, std::vector<vector<string> >* container) {
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

void edit_table(std::vector<vector<string> >* container, std::string input) {
    //parse input
    std::size_t found_num = input.find_first_of(",")+1;
    if (found_num == std::string::npos){
        cout<<"no number found, input error. Please fix and try again."<<endl;
        return;
    }

    int len = input.length();
    std::string name = input.substr(0, found_num-1);
    if (!name.length()){
        cout<<"empty name, input error"<<endl;
        return;
    }

    input = input.substr(found_num);
    std::size_t found_space = input.find_first_of(" ");
    std::string points;
    if (found_space == std::string::npos){
        points = input;
    }
    else{
        len = input.length();
        points = input.substr(0, len-found_space);
    }
    int pts = std::stoi(points);

    //if name already in table, edit points (convert, add, convert back)
    bool existing = false;

    for (auto i = container->begin(); i != container->end(); ++i) {
        string to_comp =*(i->begin());
        if (to_comp==name){
            existing = true;
            string old_points = *(i->rbegin());
            *(i->rbegin()) = to_string(stoi(old_points)+pts);
        }
    }

    //else, add new entry (convert to string)
    if (!existing){
        vector<string> row;
        row.push_back(name);
        row.push_back(points);
        container->push_back(row);
    }
}

void save_file(std::fstream* file, std::string filename, std::vector<vector<string> > table){
    file->close();
    file->open(filename, std::ofstream::out | std::ofstream::trunc);

    for(int i=0;i<table.size();i++) {
        *file<<table[i][0]<<","<<table[i][1]<<"\n";
    }
}