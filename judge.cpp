#include <iostream>
#include <string>
#include <fstream>
#include <string.h>
#include <stdlib.h>
using namespace std;
int main(int argc, char const *argv[])
{
	string standard;
	ifstream file_Standard ("JudgeSystemA/output_std");
	if (!file_Standard.is_open())
	{
		cout << "Runtime Error";
		return 0;
	}
	ifstream file_answer ("output_test");
	char Standard_answer[100];
	char Test_answer[100];
	while (!file_answer.eof()) {
		file_Standard.getline(Standard_answer, 100);
		file_answer.getline(Test_answer, 100);
		if (strcmp(Standard_answer, Test_answer))
		{
			//cout << Standard_answer << endl;
			//cout << Test_answer << endl;
			cout << "Wrong Answer";
			return 0;
		}
	}

	cout << "Accepted";
	return 0;
}
