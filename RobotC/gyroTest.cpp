#include "RTIMULib.h"

int main()
{
	int sampleCount = 0;
	int sampleRate = 0;
	RTIMU_DATA init_data;

	RTIMUSettings *settings = new RTIMUSettings("RobotC");
	RTIMU *imu = RTIMU::createIMU(settings);

	if((imu == NULL) || (imu->IMUType() == RTIMU_TYPE_NULL)){
		printf("No IMU found\n");
		exit(1);
	}


	imu->IMUInit();
	imu->setSlerpPower(0.02);
	imu->setGyroEnable(true);
	imu->setAccelEnable(true);
	imu->setCompassEnable(false);

	init_data = imu->getIMUData();

	while(1){
		usleep(imu->IMUGetPollInterval() * 1000);

		while(imu->IMURead()){
			RTIMU_Data imuData = imu->getIMUData();
			float difference = init_data.z() - imuData.z();
			printf("Heading = %f", difference * RTMATH_RAD_TO_DEGREE);
			fflush(stdout);
		}
	}
}
