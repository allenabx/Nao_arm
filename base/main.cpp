#include <iostream>
#include "RotationMatrix.h"
#include "Pose3D.h"
#include "RobotDimensions.h"
#include "controller.h"

using namespace std;

Connection* Connection::instance_ = 0;
ACT* ACT::instance_ = 0;

int main() {
    // Controller controller;
    // controller.ControlInit();
    // float angles[NUM_JOINTS];
    // Joint arm0 = RShoulderPitch;
    // // control effectors by ActHandle
    // controller.QueueAction(JID_RARM_1, 90);
    // controller.ActQueue();
    // // define of arm angle and use kinematics
    // angles[arm0 + 0] = (float)M_PI_2;
    // angles[arm0 + 1] = 0;
    // angles[arm0 + 2] = 0;
    // angles[arm0 + 3] = 0;
    // Vector3<float> rst = Kinematics(angles);
    // while(1)
    // {
    //     controller.Run();
    // }
    float angles[NUM_JOINTS];
    Joint arm0 = RShoulderPitch;
    angles[arm0 + 0] = (float)0;
    angles[arm0 + 1] = (float)0;
    angles[arm0 + 2] = -(float)0;
    angles[arm0 + 3] = -(float)0;
    Pos pos;
    pos = Kinematics(angles);
    cout << pos.x << endl;
    cout << pos.y << endl;
    cout << pos.z << endl;
    return 0;
}

