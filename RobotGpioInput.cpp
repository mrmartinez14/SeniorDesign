#include "Python.h"
#include "wiringPi.h"
#include "opencv2/opencv.hpp"
#include <stdbool.h>
bool roll;

void proxISR(){
	roll = 0;
	return;
}

int main(){
	roll = 1;
	wiringPiSetupGpio();
	pinMode(21, INPUT);
	wiringPiISR(26, INT_EDGE_FALLING, proxISR);
	printf("here\n");
	PyObject *pStateMachine, *pSMModule, *pStart;
	PyObject *pGetRolling, *pKillMotors, *pSetMotors;
        PyObject *pDoTheTurn;
	PyObject *pPyFuncName, *pPyFunc, *pStartCamera, *pGetFrame, *pGetMask, *pGetPosition, *pCleanUp;
	PyObject *pArr, *pMask, *pXCoord, *pState;
	printf("next\n");
	Py_Initialize();

	pStateMachine = PyString_FromString("state_machine2");
        pPyFuncName = PyString_FromString("py_func");

	pPyFunc = PyImport_Import(pPyFuncName);
        if(pPyFunc != NULL){
		printf("Sarah, help me \n");
//		return 0;
	}
	pSMModule = PyImport_Import(pStateMachine);
	Py_DECREF(pStateMachine);
	Py_DECREF(pPyFuncName);

	if(pSMModule != NULL){
		pStartCamera = PyObject_GetAttrString(pPyFunc, "start_camera");
		pGetFrame = PyObject_GetAttrString(pPyFunc, "get_frame");
		pGetMask = PyObject_GetAttrString(pPyFunc, "get_mask");
		pCleanUp = PyObject_GetAttrString(pPyFunc, "clean_up");
		pSetMotors = PyObject_GetAttrString(pSMModule, "set_motors");
                if(pSetMotors && PyCallable_Check(pSetMotors)){
			printf("I don't know what to do \n");
//			return 0;
		}else return 0;
		pStart = PyObject_GetAttrString(pSMModule, "start");
		pGetRolling = PyObject_GetAttrString(pSMModule, "get_rolling");
		pKillMotors = PyObject_GetAttrString(pSMModule, "kill_motors");
		pDoTheTurn = PyObject_GetAttrString(pSMModule, "do_the_turn");
		if(pStart && PyCallable_Check(pStart)){
			while(digitalRead(21) == 0){;}
			while(digitalRead(21) == 1){
				roll = 1;
				pState = PyObject_CallFunction(pStart, NULL);
				PyObject_CallFunction(pSetMotors, pState, NULL);
				while(roll){;}
				PyObject_CallFunction(pDoTheTurn, NULL);
				roll = 1;
				while(roll){;}
			}
			PyObject_CallFunction(pKillMotors,NULL);
		}
	}

	return 0;
}
