#include <stdio.h>
#include "wiringPi.h"
#include <stdbool.h>

class motors
{
	private:

	// Pin assignments
	const static int motor1 = 12;
	const static int motor2 = 13;
	const static int m1enable = 22;
	const static int m1dir = 24;
	const static int m2enable = 23;
	const static int m2dir = 25;

	// Holds direction, 0 forward, 1 back
	int dir1;
	int dir2;

	public:

	// Max pwm duty cycle
	const static int MAX_SPEED = 480;

	motors()
	{
		dir1 = 0;
		dir2 = 0;
		wiringPiSetupGpio();
		pinMode(motor1, PWM_OUTPUT);
		pinMode(motor2, PWM_OUTPUT);

		pwmSetMode(PWM_MODE_MS);
		pwmSetRange(MAX_SPEED);
		pwmSetClock(2);

		pinMode(m1enable, OUTPUT);
		pinMode(m1dir, OUTPUT);
		pinMode(m2enable, OUTPUT);
		pinMode(m2dir, OUTPUT);
	}

	void enable()
	{
		digitalWrite(m1enable, 1);
		digitalWrite(m2enable, 1);
	}

	void enablem1()
	{
		digitalWrite(m1enable, 1);
	}

	void enablem2()
	{
		digitalWrite(m2enable, 1);
	}

	void disable()
	{
		digitalWrite(m1enable, 0);
		digitalWrite(m2enable, 0);
	}

	void disablem1()
	{
		digitalWrite(m1enable, 0);
	}

	void disablem2()
	{
		digitalWrite(m2enable, 0);
	}

	void setM1Speed(int m1)
	{
		if(m1 < 0){
			m1 = -m1;
			dir1 = 1;
		}else{
			dir1 = 0;
		}

		if(m1 > MAX_SPEED){
			m1 = MAX_SPEED;
		}

		digitalWrite(m1dir, dir1);
		pwmWrite(motor1, m1);
	}

	void setM2Speed(int m2)
	{
		if(m2 < 0){
			m2 = -m2;
			dir2 = 1;
		}else{
			dir2 = 0;
		}

		if(m2 > MAX_SPEED){
			m2 = MAX_SPEED;
		}

		digitalWrite(m2dir, dir2);
		pwmWrite(motor2, m2);
	}


	void setSpeeds(int m1, int m2)
	{
		setM1Speed(m1);
		setM2Speed(m2);
	}

};
