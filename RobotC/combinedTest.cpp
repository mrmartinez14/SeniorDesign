#include "RTIMULib.h"
#include "math.h"
#include "motorRPi.cpp"
#include <signal.h>
#include <stdio.h>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

bool flag = 0;
bool prox = 0;

void progStop(int sig){
	flag = 1;
}

void SetTurnFlag(){
	prox = 1;
}

int main()
{
	motors *m = new motors();

	// Interrupt setup
	signal(SIGINT, progStop);
	wiringPiISR(26, INT_EDGE_FALLING, SetTurnFlag);

	// Camera Setup
	VideoCapture cap(0);
	if(!cap.isOpened()){
		cerr << "ERROR: unable to open camera" << endl;
		return 0;
	}
	cap.set(CV_CAP_PROP_FRAME_WIDTH, 1280);
	cap.set(CV_CAP_PROP_FRAME_HEIGHT, 720);
	printf("w = %d, h = %d\n", (int)cap.get(CV_CAP_PROP_FRAME_WIDTH), (int)cap.get(CV_CAP_PROP_FRAME_HEIGHT));
	Mat frame, hsv;
	Scalar minYellow = Scalar(20, 60, 60);
	Scalar maxYellow = Scalar(25, 200,200);
	vector<vector<Point> > cnts;
	double xCoord = 0;
	int saw = 0;

	// IMU setup
	int sampleCount = 0;
	int sampleRate = 0;
	float tolerance = 2;
	double read;
	double angAvg;
	float correct = 0;
	float difference;
	RTIMU_DATA init_data;

	RTIMUSettings *settings = new RTIMUSettings("RTIMULib");
	RTIMU *imu = RTIMU::createIMU(settings);

	if((imu == NULL) || (imu->IMUType() == RTIMU_TYPE_NULL)){
		printf("No IMU found\n");
		exit(1);
	}

	imu->IMUInit();
	imu->setSlerpPower(0.02);
	imu->setGyroEnable(true);
	imu->setAccelEnable(true);
	imu->setCompassEnable(true);

	// Motor setup
	int DCR = 220;// 250;
	int spR = 0;
	int DCL = 300;// 300;
//	m->enable();
	m->setSpeeds(DCL,DCR);
	sleep(2.5);

	// Getting inital angle read
	for(int i = 0; i < 10; i++){
		usleep(imu->IMUGetPollInterval() * 1000);
		while(imu->IMURead()){
			init_data = imu->getIMUData();
		}
	}

	// Print initial angle
	printf("Init %f\n", init_data.fusionPose.z()*RTMATH_RAD_TO_DEGREE);

	while(!flag){
		// Check prox flag to turn
		if(prox == 1){
			printf("prox = %d\n", prox);
			m->setSpeeds(0,480);
			//sleep(2); ARC floor
			usleep(1500000);
			m->setSpeeds(DCR,DCL);
			prox = 0;
		}

		//start image processing
		cap >> frame;
		if(frame.empty()){
			cout << "no picture" << endl;
		}else{
			cvtColor(frame, hsv, cv::COLOR_BGR2HSV);
			Mat resHSV, maskHSV, bwHSV;
			inRange(hsv, minYellow, maxYellow, maskHSV);
			erode(maskHSV, resHSV, Mat(), Point(-1,-1), 2);
			dilate(resHSV, maskHSV, Mat(), Point(-1,-1), 2);
			findContours(resHSV, cnts, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
			double largestArea = 0;
			double x = 0;
			int lrgstContourIndex = 0;
			if(cnts.size() > 0){
				for(int i = 0; i < cnts.size(); i++){
					double a = contourArea(cnts[i], false);
					if(a > largestArea){
						largestArea = a;
						lrgstContourIndex = i;
					}
				}
				vector<Point> roi = cnts[lrgstContourIndex];
				for(int i = 0; i < roi.size(); i++){
					x += roi[i].x;
				}
				xCoord = x/roi.size();
				saw ++;
			}else{
				saw = 0;
				xCoord = -1;
			}
		}

		read = 0;
		int samp =0;
		if(saw < 3){
		usleep(imu->IMUGetPollInterval() * 1000);
		RTIMU_DATA imuData;
//		for(int i = 0; i < 3; i++){
		while(imu->IMURead()){
			imuData = imu->getIMUData();
			//difference = (init_data.fusionPose.z() - imuData.fusionPose.z())* RTMATH_RAD_TO_DEGREE;
			//difference = imuData.fusionPose.z()* RTMATH_RAD_TO_DEGREE;
			//printf("Heading = %f\r", difference);
			read = read + imuData.fusionPose.z()*RTMATH_RAD_TO_DEGREE;
			samp++;
		}
//		}
//		printf("xCoord = %f, angAvg = %f\n", xCoord, imuData.fusionPose.z());
		angAvg = read;//double(samp);
		if(read != 0){
		correct = (init_data.fusionPose.z()*RTMATH_RAD_TO_DEGREE-imuData.fusionPose.z())*25;
		}
		else
			correct = 0;
		}
		printf("xCoord = %f\n", xCoord);
//		correct = (85.0-angAvg)*25;
//		printf("correct = %f\r",correct);
		spR = DCR-correct;
		m->setSpeeds(DCL, spR);
	}
	printf("\nEnding program\n");
	m->disable();
	m->setSpeeds(0,0);
	cap.release();
}
