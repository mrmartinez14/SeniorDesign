#include "RTIMULib.h"
#include "math.h"
#include "motorRPi.cpp"
#include <signal.h>

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
	signal(SIGINT, progStop);
	motors *m = new motors();
	wiringPiISR(26, INT_EDGE_FALLING, SetTurnFlag);
	m->enable();
	int sampleCount = 0;
	int sampleRate = 0;
	float tolerance = 2;
	int DCR = 220;// 250;
	int spR = 0;
	int DCL = 300;// 300;
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
	m->enable();
	m->setSpeeds(DCL,DCR);
	sleep(2.5);

	for(int i = 0; i < 10; i++){
		usleep(imu->IMUGetPollInterval() * 1000);
		while(imu->IMURead()){
			init_data = imu->getIMUData();
		}
	}

	printf("Init %f\n", init_data.fusionPose.z()*RTMATH_RAD_TO_DEGREE);
	while(!flag){
		if(prox == 1){
			printf("prox = %d\n", prox);
			m->setSpeeds(0,480);
			//sleep(2); ARC floor
			usleep(1500000);
			m->setSpeeds(DCR,DCL);
			prox = 0;
		}
		read = 0;
		int samp =0;

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
			fflush(stdout);
		}
//		}
		angAvg = read;//double(samp);
		printf("prox = %d, angAvg = %f\r",prox,imuData.fusionPose.z());
		if(read != 0){
		correct = (init_data.fusionPose.z()*RTMATH_RAD_TO_DEGREE-imuData.fusionPose.z())*25;
		}
		else
			correct = 0;
//		correct = (85.0-angAvg)*25;
//		printf("correct = %f\r",correct);
		spR = DCR-correct;
		m->setSpeeds(DCL, spR);
	}
	printf("\nEnding program\n");
	m->disable();
	m->setSpeeds(0,0);
}
