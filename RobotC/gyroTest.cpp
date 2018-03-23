#include "RTIMULib.h"
#include "math.h"
#include "motorRPi.cpp"
#include <signal.h>

bool flag = 0;

void progStop(int sig){
	flag = 1;
}

int main()
{
	signal(SIGINT, progStop);
	motors *m = new motors();
	m->enable();
	int sampleCount = 0;
	int sampleRate = 0;
	float tolerance = 4;
	int DCR = 0;
	int DCL = 0;
	int speedR = 0;
	int speedL = 0;
	int pathcheck = 0;
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

	for(int i = 0; i < 10; i++){
		while(imu->IMURead()){
			init_data = imu->getIMUData();
		}
	}
	printf("Init %f\n", init_data.fusionPose.z());
	while(!flag){

		usleep(imu->IMUGetPollInterval() * 1000);

		while(imu->IMURead()){
			RTIMU_DATA imuData = imu->getIMUData();
			difference = (init_data.fusionPose.z() - imuData.fusionPose.z())* RTMATH_RAD_TO_DEGREE;
			//difference = imuData.fusionPose.z()* RTMATH_RAD_TO_DEGREE;
			printf("Heading = %f\r", difference);
			fflush(stdout);
		}
		if(abs(difference)<tolerance){
			DCR = speedR;
			DCL = speedL;
			pathcheck++;
			printf("heading straight\n");
		}
		else if(difference>tolerance){
			DCR = speedR;
			DCL = speedL-48;
			pathcheck = 0;
			printf("heading right\n");
		}
		else if(difference<-tolerance){
			DCR = speedR-48;
			DCL = speedL;
			pathcheck = 0;
			printf("heading left\n");
		}
		if(pathcheck>5){
			speedR+=24;
			speedL+=24;
		}
		m->setSpeeds(DCL, DCR);
		sleep(1);
	}
	printf("\nEnding program\n");
	m->disable();
	m->setSpeeds(0,0);
}
