#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <signal.h>

using namespace cv;
using namespace std;

bool flag = 0;

void progStop(int sig){
	flag = 1;
}

int main(int argc, char ** argv)
{
	signal(SIGINT, progStop);
	VideoCapture cap(0);
	if (!cap.isOpened()){
		cerr << "ERROR: Unable to open camera" << endl;
		return 0;
	}
	Mat frame, hsv;
	Scalar minYellow = Scalar(20,60,60);
	Scalar maxYellow = Scalar(25,200,200);
	vector<vector<Point> > cnts;

	while(!flag){
		cap >> frame;
		if(frame.empty()){
			cout<< "no picture" << endl;
			break;
		}
		cvtColor(frame, hsv, cv::COLOR_BGR2HSV);
		Mat resHSV, maskHSV, bwHSV;
		inRange(hsv, minYellow, maxYellow, maskHSV);
		erode(maskHSV, resHSV, Mat(), Point(-1,-1), 2);
		dilate(resHSV, maskHSV, Mat(), Point(-1,-1),2);
		findContours(resHSV, cnts, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
		double largestArea = 0;
		double xCoord = 0;
		int largestContourIndex = 0;
		if(cnts.size()>0){
			for( int i = 0; i< cnts.size(); i++ ){ // iterate through each contour.
				double a=contourArea( cnts[i],false);  //  Find the area of contour
				if(a>largestArea){
					largestArea=a;
					largestContourIndex=i;//Store the index of largest contour
				}
			}
			vector<Point> roi = cnts[largestContourIndex];
			for(int i = 0; i < roi.size(); i++){
				xCoord += roi[i].x;
			}
			xCoord = xCoord / roi.size();
			cout << xCoord << endl;
		}
	}
	cout << "Closing the camera" << endl;
	cap.release();
	return 0;
}
